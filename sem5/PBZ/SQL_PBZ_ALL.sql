CREATE TABLE IF NOT EXISTS owners (
	license_number VARCHAR(20) PRIMARY KEY,
	full_name VARCHAR(100) NOT NULL,
	address TEXT NOT NULL,
	birth_year INTEGER NOT NULL CHECK (birth_year > 1920 AND 
        birth_year <= EXTRACT(YEAR FROM CURRENT_DATE) - 18),
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


SELECT * FROM owners ORDER BY full_name;


SELECT c.*, e.*, o.full_name 
	FROM cars c 
	LEFT JOIN engines e ON c.engine_number = e.engine_number
	LEFT JOIN owners o ON c.owner_license_number = o.license_number 
	ORDER BY c.license_plate;


SELECT * FROM engines ORDER BY performance;



SELECT * FROM inspectors ORDER BY full_name;

INSERT INTO inspectors (full_name, insp_position, insp_rank)
     VALUES (%s, %s, %s);


SELECT * FROM inspections ORDER BY inspection_date;


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
CREATE OR REPLACE PROCEDURE add_engine(
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


CREATE OR REPLACE PROCEDURE add_owner(
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


CREATE OR REPLACE PROCEDURE add_car(
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


CREATE OR REPLACE PROCEDURE delete_car(v_tech_passport_number VARCHAR(50))
LANGUAGE plpgsql
AS $$
DECLARE
    v_engine_number VARCHAR(50);
    engine_usage_count INTEGER;
BEGIN
    SELECT engine_number INTO v_engine_number
    FROM cars 
    WHERE tech_passport_number = v_tech_passport_number;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Автомобиль с техпаспортом % не существует', tech_passport_number;
    END IF;
    
    SELECT COUNT(*) INTO engine_usage_count
    FROM cars 
    WHERE engine_number = v_engine_number;
    
    DELETE FROM cars WHERE tech_passport_number = tech_passport_number;
    
    IF engine_usage_count = 1 THEN
        DELETE FROM engines WHERE engine_number = v_engine_number;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_owner(v_license_number VARCHAR(20))
LANGUAGE plpgsql
AS $$
DECLARE
    engine_numbers TEXT[];
BEGIN
    IF NOT EXISTS (SELECT 1 FROM owners WHERE license_number = v_license_number) THEN
        RAISE EXCEPTION 'Владелец с номером % не существует', license_number;
    END IF;

    SELECT array_agg(DISTINCT c.engine_number) INTO engine_numbers
    FROM cars c 
    WHERE c.owner_license_number = v_license_number
      AND NOT EXISTS (
          SELECT 1 FROM cars c2 
          WHERE c2.engine_number = c.engine_number 
          AND c2.owner_license_number != v_license_number
      );

    DELETE FROM owners WHERE license_number = v_license_number;

    IF engine_numbers IS NOT NULL THEN
        DELETE FROM engines 
        WHERE engine_number = ANY(engine_numbers);
    END IF;
END;
$$;


--Добавление/редактирование/удаление информации о проведенном осмотре.
CREATE OR REPLACE PROCEDURE add_inspection(
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

CREATE OR REPLACE PROCEDURE delete_inspection(inspection_id INTEGER)
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
CREATE OR REPLACE PROCEDURE delete_inspector(inspector_id INTEGER)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM inspectors WHERE id = inspector_id) THEN
        RAISE EXCEPTION 'Инспектор с id % не существует', inspector_id;
    END IF;
    
    DELETE FROM inspectors WHERE id = inspector_id;
END;
$$;



--обновление осмотра
CREATE OR REPLACE PROCEDURE update_inspection(
	v_id INTEGER,
	v_car_license_plate VARCHAR(15),
	v_inspector_id INTEGER,
	v_inspection_date DATE,
	v_inspection_result BOOLEAN,
	v_conclusion TEXT
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM inspections WHERE id = v_id) THEN
        RAISE EXCEPTION 'Осмотр с id % не существует', v_id;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM cars WHERE license_plate = v_car_license_plate) THEN
        RAISE EXCEPTION 'Автомобиль с номером % не существует', v_car_license_plate;
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM inspectors WHERE id = v_inspector_id) THEN
        RAISE EXCEPTION 'Инспектор с id % не существует', v_inspector_id;
    END IF;
    
    UPDATE inspections 
    SET car_license_plate = v_car_license_plate,
        inspector_id = v_inspector_id,
        inspection_date = v_inspection_date,
        inspection_result = v_inspection_result,
        conclusion = v_conclusion
    WHERE id = v_id;
END;
$$;


CREATE OR REPLACE PROCEDURE update_owner(
	v_license_number VARCHAR(20),
	v_full_name VARCHAR(100),
	v_address TEXT,
	v_birth_year INTEGER,
	v_gender VARCHAR(10)	
)
LANGUAGE plpgsql 
AS $$
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM owners WHERE license_number = v_license_number) THEN
        RAISE EXCEPTION 'Владелец с номером % не существует', v_license_number;
    END IF;
    
    UPDATE owners 
    SET full_name = v_full_name, 
        address = v_address, 
        birth_year = v_birth_year, 
        gender = v_gender
    WHERE license_number = v_license_number;
END;
$$;



CREATE OR REPLACE PROCEDURE update_inspector(
	v_id INTEGER,
	v_full_name VARCHAR(100),
	v_insp_position VARCHAR(50),
	v_insp_rank VARCHAR(50)
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM inspectors WHERE id = v_id) THEN
        RAISE EXCEPTION 'Инспектор с id % не существует', v_id;
    END IF;
    
    UPDATE inspectors 
    SET full_name = v_full_name,
        insp_position = v_insp_position,
        insp_rank = v_insp_rank
    WHERE id = v_id;
END;
$$;



CREATE OR REPLACE PROCEDURE update_car_with_engine(
    v_tech_passport_number VARCHAR(50),
    v_license_plate VARCHAR(15),
    v_color VARCHAR(30),
    v_brand VARCHAR(50),
    v_owner_license_number VARCHAR(20),
    v_engine_number VARCHAR(50),
    v_country VARCHAR(30),
    v_performance INTEGER
)
LANGUAGE plpgsql
AS $$
DECLARE
    old_engine_number VARCHAR(50);
BEGIN
    SELECT engine_number INTO old_engine_number 
    FROM cars WHERE tech_passport_number = v_tech_passport_number;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Автомобиль с техпаспортом % не существует', v_tech_passport_number;
    END IF;

    IF NOT EXISTS (SELECT 1 FROM owners WHERE license_number = v_owner_license_number) THEN
        RAISE EXCEPTION 'Владелец с номером % не существует', v_owner_license_number;
    END IF;

    IF EXISTS (SELECT 1 FROM engines WHERE engine_number = v_engine_number) THEN
        UPDATE engines 
        SET country = v_country, 
            performance = v_performance
        WHERE engine_number = v_engine_number;
    ELSE
        INSERT INTO engines (engine_number, country, performance)
        VALUES (v_engine_number, v_country, v_performance);
    END IF;

    UPDATE cars 
    SET license_plate = v_license_plate,
        engine_number = v_engine_number,
        color = v_color,
        brand = v_brand,
        owner_license_number = v_owner_license_number
    WHERE tech_passport_number = v_tech_passport_number;

    IF old_engine_number != v_engine_number THEN
        DELETE FROM engines 
        WHERE engine_number = old_engine_number 
        AND NOT EXISTS (SELECT 1 FROM cars WHERE engine_number = old_engine_number);
    END IF;
END;
$$;
