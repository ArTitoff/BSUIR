CREATE TABLE IF NOT EXISTS owners (
	license_number VARCHAR(20) PRIMARY KEY,
	full_name VARCHAR(100) NOT NULL,
	address TEXT NOT NULL,
	birth_year INTEGER NOT NULL,
	gender VARCHAR(10) NOT NULL
);


CREATE TABLE IF NOT EXISTS cars (
	tech_passport_number VARCHAR(50) PRIMARY KEY,
	license_plate VARCHAR(15) UNIQUE NOT NULL,
	engine_number VARCHAR(50) REFERENCES engines(engine_number) ON UPDATE CASCADE ON DELETE CASCADE,
	color VARCHAR(30) NOT NULL,
	brand VARCHAR(50) NOT NULL,
	owner_license_number VARCHAR(20) REFERENCES owners(license_number) ON UPDATE CASCADE ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS inspectors (
	id SERIAL PRIMARY KEY,
	full_name VARCHAR(100) NOT NULL,
	insp_position VARCHAR(50) NOT NULL,
	insp_rank VARCHAR(50) NOT NULL
);


CREATE TABLE IF NOT EXISTS inspections (
	id SERIAL PRIMARY KEY,
	car_license_plate VARCHAR(15) REFERENCES cars(license_plate) ON UPDATE CASCADE ON DELETE CASCADE,
	inspector_id INTEGER REFERENCES inspectors(id) ON UPDATE CASCADE ON DELETE CASCADE,
	inspection_date DATE NOT NULL,
	inspection_result BOOLEAN NOT NULL,
	conclusion TEXT
);


CREATE TABLE IF NOT EXISTS engines (
	engine_number VARCHAR(50) PRIMARY KEY,
	country VARCHAR(30) NOT NULL,
	performance INT NOT NULL
);


INSERT INTO owners (license_number, full_name, address, birth_year, gender)
	VALUES (%s, %s, %s, %s, %s);


SELECT * FROM owners ORDER BY full_name;


UPDATE owners 
	SET license_number=%s, full_name=%s, address=%s, birth_year=%s, gender=%s
	WHERE license_number=%s;


DELETE FROM owners WHERE license_number=%s;


INSERT INTO cars (license_plate, engine_number, color, brand, tech_passport_number, owner_license_number)
    VALUES (%s, %s, %s, %s, %s, %s);


SELECT c.*, e.*, o.full_name 
	FROM cars c 
	LEFT JOIN engines e ON c.engine_number = e.engine_number
	LEFT JOIN owners o ON c.owner_license_number = o.license_number 
	ORDER BY c.license_plate;


UPDATE cars 
	SET license_plate=%s, engine_number=%s, color=%s, brand=%s, tech_passport_number=%s, owner_license_number=%s
	WHERE tech_passport_number=%s;


DELETE FROM cars WHERE tech_passport_number=%s;


INSERT INTO engines (engine_number, country, performance)
	VALUES (%s, %s, %s);


SELECT * FROM engines ORDER BY performance;


UPDATE engines 
	SET engine_number=%s, country=%s, performance=%s
	WHERE engine_number=%s;


DELETE FROM engines WHERE engine_number=%s;


INSERT INTO inspectors (full_name, insp_position, insp_rank)
     VALUES (%s, %s, %s);


SELECT * FROM inspectors ORDER BY full_name;


UPDATE inspectors 
	SET full_name=%s, insp_position=%s, insp_rank=%s
	WHERE id=%s;


DELETE FROM inspectors WHERE id=%s;


INSERT INTO inspections (car_license_plate, inspector_id, inspection_date, inspection_result, conclusion)
      VALUES (%s, %s, %s, %s, %s);


SELECT * FROM inspections ORDER BY inspection_date;


UPDATE inspections 
	SET car_license_plate=%s, inspector_id=%s, inspection_date=%s, inspection_result=%s, conclusion=%s
	WHERE id=%s;	


DELETE FROM inspections WHERE id=%s;




--Расчет количество автомобилей, прошедших техосмотр за заданный промежуток времени с разбивкой по дням
SELECT inspection_date, COUNT(*) as count
	FROM inspections
	WHERE inspection_date BETWEEN %s AND %s
	GROUP BY inspection_date
	ORDER BY inspection_date;





--Просмотр списка сотрудников ГАИ, проводивших осмотр на заданную дату: ФИО, звание сотрудника, госномера автомобилей, которые он осматривал.
SELECT ins.full_name, ins.insp_rank, array_agg(DISTINCT i.car_license_plate) as cars
	FROM inspectors ins
	JOIN inspections i ON ins.id = i.inspector_id
	WHERE i.inspection_date = %s
	GROUP BY ins.id, ins.full_name, ins.insp_rank;

--Этот же запрос только через функцию и обработку исключений
CREATE OR REPLACE FUNCTION check_list_of_inspectors_on_date(insp_date DATE)
	RETURNS TABLE (    
	full_name VARCHAR(100),
	insp_rank VARCHAR(50),
	cars TEXT[] )
LANGUAGE plpgsql AS $$	
BEGIN
	IF NOT EXISTS (SELECT 1 FROM inspections WHERE inspection_date = insp_date) THEN
		RAISE EXCEPTION 'Осмотров на заданную дату % нет', insp_date;
    	END IF;
    	
    	RETURN QUERY
	SELECT ins.full_name, ins.insp_rank, array_agg(DISTINCT i.car_license_plate) as cars
		FROM inspectors ins
		JOIN inspections i ON ins.id = i.inspector_id
		WHERE i.inspection_date = insp_date
		GROUP BY ins.id, ins.full_name, ins.insp_rank;
END; 
$$;




--Просмотр истории прохождения осмотров заданным автомобилем (номер двигателя) – дата прохождения, результат.
SELECT i.car_license_plate, i.inspection_date, i.inspection_result, i.conclusion, ins.full_name, ins.insp_rank
	FROM inspections i
	JOIN cars c ON i.car_license_plate = c.license_plate
	JOIN inspectors ins ON i.inspector_id = ins.id
	WHERE c.engine_number = %s
	ORDER BY i.inspection_date;

--Этот же запрос только через функцию и обработку исключений
CREATE OR REPLACE FUNCTION check_inspections_hystory_by_engine(engine_num VARCHAR(50))
	RETURNS TABLE (	car_license_plate VARCHAR(15),
			inspection_date DATE,
			inspection_result BOOL, 
			conclusion TEXT, 
			full_name VARCHAR(100),
			insp_rank VARCHAR(50))
LANGUAGE plpgsql AS $$	
BEGIN
	IF NOT EXISTS (SELECT 1 FROM engines WHERE engine_number = engine_num) THEN
		RAISE EXCEPTION 'Двигателя с номером % нет', engine_num;
	END IF;
	
	    -- Проверка существования осмотров
	IF NOT EXISTS (
		SELECT 1 FROM inspections i 
		JOIN cars c ON i.car_license_plate = c.license_plate 
		WHERE c.engine_number = engine_num
		) THEN
	   RAISE NOTICE 'Для двигателя % нет истории осмотров', engine_num;
	END IF;
	
	RETURN QUERY
	SELECT i.car_license_plate, i.inspection_date, i.inspection_result, i.conclusion, ins.full_name, ins.insp_rank
		FROM inspections i
		JOIN cars c ON i.car_license_plate = c.license_plate
		JOIN inspectors ins ON i.inspector_id = ins.id
		WHERE c.engine_number = engine_num
		ORDER BY i.inspection_date;
END;
$$;




--Индексы
CREATE INDEX idx_inspection_date ON inspections(inspection_date);

CREATE INDEX idx_inspections_date_and_insp_id ON inspections(inspection_date, inspector_id);




--Функция и триггер для контроля осмотров не больше 10 в день
CREATE OR REPLACE FUNCTION check_daily_inspector_inspections()
RETURNS TRIGGER AS $$
	DECLARE inspections_count INT;
BEGIN
	SELECT COUNT(*) INTO inspections_count
	FROM inspections i
	WHERE i.inspection_date = NEW.inspection_date 
		AND i.inspector_id = NEW.inspector_id 
		AND (TG_OP = 'INSERT' OR i.id != NEW.id);
	
	IF inspections_count >= 10 THEN
		RAISE EXCEPTION 'Инспектор с id: % не может иметь больше 10 осмотров в день', NEW.inspector_id;
	END IF;
	
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER daily_inspections_count_check
	BEFORE INSERT OR UPDATE ON inspections
	FOR EACH ROW
	EXECUTE FUNCTION check_daily_inspector_inspections();





--Добавление/удаление информации о владельцах автомобилей и их транспортных средствах 
--(вместо обычных запросов/можно заменить на эти процедуры в дальнейшем).
CREATE PROCEDURE add_engine(
    v_engine_number VARCHAR(50),
    v_country VARCHAR(30),
    v_performance INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM engines WHERE engine_number = v_engine_number) THEN
        RAISE EXCEPTION 'Двигатель с номером % уже существует', v_engine_number;
    END IF;
    
    INSERT INTO engines (engine_number, country, performance)
    VALUES (v_engine_number, v_country, v_performance);
END;
$$;


CREATE PROCEDURE add_owner(
    v_license_number VARCHAR(20),
    v_full_name VARCHAR(100),
    v_address TEXT,
    v_birth_year INTEGER,
    v_gender VARCHAR(10)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM owners WHERE license_number = v_license_number) THEN
        RAISE EXCEPTION 'Владелец с номером % уже существует', v_license_number;
    END IF;
    
    INSERT INTO owners (license_number, full_name, address, birth_year, gender)
    VALUES (v_license_number, v_full_name, v_address, v_birth_year, v_gender);
END;
$$;


CREATE PROCEDURE add_car(
    v_tech_passport_number VARCHAR(50),
    v_license_plate VARCHAR(15),
    v_engine_number VARCHAR(50),
    v_color VARCHAR(30),
    v_brand VARCHAR(50),
    v_owner_license_number VARCHAR(20)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM cars WHERE tech_passport_number = v_tech_passport_number) THEN
        RAISE EXCEPTION 'Автомобиль с техпаспортом % уже существует', v_tech_passport_number;
    END IF;
    
    IF EXISTS (SELECT 1 FROM cars WHERE license_plate = v_license_plate) THEN
        RAISE EXCEPTION 'Автомобиль с номером % уже существует', v_license_plate;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM engines WHERE engine_number = v_engine_number) THEN
        RAISE EXCEPTION 'Двигатель с номером % не существует', v_engine_number;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM owners WHERE license_number = v_owner_license_number) THEN
        RAISE EXCEPTION 'Владелец с номером % не существует', v_owner_license_number;
    END IF;
    
    INSERT INTO cars (tech_passport_number, license_plate, engine_number, color, brand, owner_license_number)
    VALUES (v_tech_passport_number, v_license_plate, v_engine_number, v_color, v_brand, v_owner_license_number);
END;
$$;


CREATE PROCEDURE add_owner_with_car(license_number VARCHAR(20),
				    full_name VARCHAR(100),
				    address TEXT,
				    birth_year INTEGER,
				    gender VARCHAR(10),
				    tech_passport_number VARCHAR(50),
				    license_plate VARCHAR(15),
				    engine_number VARCHAR(50),
				    color VARCHAR(30),
				    brand VARCHAR(50),
				    country VARCHAR(30),
				    performance INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    CALL add_engine(engine_number, country, performance);
    CALL add_owner(license_number, full_name, address, birth_year, gender);
    CALL add_car(tech_passport_number, license_plate, engine_number, color, brand, license_number);
END;
$$;


CREATE PROCEDURE delete_car(tech_passport_number VARCHAR(50))
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM cars WHERE tech_passport_number = tech_passport_number) THEN
        RAISE EXCEPTION 'Автомобиль с техпаспортом % не существует', tech_passport_number;
    END IF;
    
    DELETE FROM cars WHERE tech_passport_number = tech_passport_number;
END;
$$;

CREATE PROCEDURE delete_owner(license_number VARCHAR(20))
LANGUAGE plpgsql
AS $$
DECLARE
    car_count INTEGER;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM owners WHERE license_number = license_number) THEN
        RAISE EXCEPTION 'Владелец с номером % не существует', license_number;
    END IF;

    DELETE FROM owners WHERE license_number = license_number;
END;
$$;

CREATE PROCEDURE delete_engine(engine_number VARCHAR(50))
LANGUAGE plpgsql
AS $$
DECLARE
    car_count INTEGER;
BEGIN
    IF NOT EXISTS (SELECT 1 FROM engines WHERE engine_number = engine_number) THEN
        RAISE EXCEPTION 'Двигатель с номером % не существует', engine_number;
    END IF;
    
    DELETE FROM engines WHERE engine_number = engine_number;
END;
$$;





--Добавление/редактирование/удаление информации о проведенном осмотре.
CREATE PROCEDURE add_inspection(
    v_car_license_plate VARCHAR(15),
    v_inspector_id INTEGER,
    v_inspection_date DATE,
    v_inspection_result BOOLEAN,
    v_conclusion TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM cars WHERE license_plate = v_car_license_plate) THEN
        RAISE EXCEPTION 'Автомобиль с номером % не существует', v_car_license_plate;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM inspectors WHERE id = v_inspector_id) THEN
        RAISE EXCEPTION 'Инспектор с id % не существует', v_inspector_id;
    END IF;
    
    INSERT INTO inspections (car_license_plate, inspector_id, inspection_date, inspection_result, conclusion)
    VALUES (v_car_license_plate, v_inspector_id, v_inspection_date, v_inspection_result, v_conclusion);
END;
$$;

CREATE PROCEDURE delete_inspection(inspection_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM inspections WHERE id = inspection_id) THEN
        RAISE EXCEPTION 'Осмотр с id % не существует', inspection_id;
    END IF;
    
    DELETE FROM inspections WHERE id = inspection_id;
END;
$$;





--удаление информации о сотрудниках ГАИ.
CREATE PROCEDURE delete_inspector(inspector_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM inspections WHERE id = inspection_id) THEN
        RAISE EXCEPTION 'Осмотр с id % не существует', inspection_id;
    END IF;
    
    DELETE FROM inspections WHERE id = inspection_id;
END;
$$;
