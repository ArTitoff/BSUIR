class Client:
    def __init__(self, name: str, surname: str, otchestvo: str, account_num: int, address: str,
                 mob_telephone: str, home_telephone: str):
        self.__name = name
        self.__surname = surname
        self.__otchestvo = otchestvo
        self.__account_num = account_num
        self.__address = address
        self.__mob_telephone = mob_telephone
        self.__home_telephone = home_telephone

    def get_name(self) -> str:
        return self.__name

    def get_surname(self) -> str:
        return self.__surname

    def get_otchestvo(self) -> str:
        return self.__otchestvo

    def get_account_num(self) -> int:
        return self.__account_num

    def get_address(self) -> str:
        return self.__address

    def get_mob_telephone(self) -> str:
        return self.__mob_telephone

    def get_home_telephone(self) -> str:
        return self.__home_telephone


class RecordModel:
    def __init__(self):
        self.clients: list[Client] = []

    def get_clients(self):
        return self.clients
    
    def add_client(self, client):
        self.clients.append(client)

    def find_clients_by_phone_or_surname(self, phone=None, surname=None) -> list[Client]:
        result = []
        normalized_surname = surname.lower().strip() if surname else None
        
        for client in self.clients:
            client_surname = client.get_surname().lower().strip()
            if (phone and (client.get_mob_telephone() == phone or client.get_home_telephone() == phone)) or \
            (normalized_surname and client_surname == normalized_surname):
                result.append(client)
        return result

    def find_clients_by_account_or_address(self, account_num=None, address=None) -> list[Client]:
        result = []
        normalized_address = address.lower().strip() if address else None
        
        for client in self.clients:
            if (account_num is not None and client.get_account_num() == account_num) or \
            (normalized_address and client.get_address().lower().strip() == normalized_address):
                result.append(client)
        return result

    def find_clients_by_fio_or_digits(self, name=None, surname=None, otchestvo=None, digits=None) -> list[Client]:
        result = []
        normalized_name = name.lower().strip() if name else None
        normalized_surname = surname.lower().strip() if surname else None
        normalized_otchestvo = otchestvo.lower().strip() if otchestvo else None
        
        for client in self.clients:
            home_telephone = client.get_home_telephone().replace("-", "")
            name_match = not normalized_name or client.get_name().lower().strip() == normalized_name
            surname_match = not normalized_surname or client.get_surname().lower().strip() == normalized_surname
            otchestvo_match = not normalized_otchestvo or client.get_otchestvo().lower().strip() == normalized_otchestvo
            digits_match = not digits or (digits in client.get_mob_telephone() or digits in home_telephone)
            
            if name_match and surname_match and otchestvo_match and digits_match:
                result.append(client)
        return result

    def delete_clients_by_phone_or_surname(self, phone=None, surname=None) -> int:
        original_count = len(self.clients)
        normalized_surname = surname.lower().strip() if surname else None
        
        self.clients = [
            client for client in self.clients
            if not (
                (phone and (client.get_mob_telephone() == phone or client.get_home_telephone() == phone)) or
                (normalized_surname and client.get_surname().lower().strip() == normalized_surname)
            )
        ]
        return original_count - len(self.clients)

    def delete_clients_by_account_or_address(self, account_num=None, address=None) -> int:
        original_count = len(self.clients)
        
        if address is not None:
            normalized_address = address.lower().strip()
        self.clients = [
            client for client in self.clients
            if not (
                (account_num is not None and client.get_account_num() == account_num) or
                (address is not None and client.get_address().lower().strip() == normalized_address)
            )
        ]
        
        return original_count - len(self.clients)
    
    def delete_clients_by_fio_or_digits(self, name=None, surname=None, otchestvo=None, digits=None) -> int:
        original_count = len(self.clients)
        normalized_name = name.lower().strip() if name else None
        normalized_surname = surname.lower().strip() if surname else None
        normalized_otchestvo = otchestvo.lower().strip() if otchestvo else None
        
        self.clients = [
            client for client in self.clients
            if not (
                (not normalized_name or client.get_name().lower().strip() == normalized_name) and
                (not normalized_surname or client.get_surname().lower().strip() == normalized_surname) and
                (not normalized_otchestvo or client.get_otchestvo().lower().strip() == normalized_otchestvo) and
                (digits and (digits in client.get_mob_telephone() or digits in client.get_home_telephone().replace("-", "")))
            )
        ]
        return original_count - len(self.clients)
