
class WrongSettings(Exception):
    def __init__(self,msg):
        super().__init__(msg)


class _base(type):
    def __new__(cls,name,base,dic):
        if name == "Spreadsheet_config":
            perform_sp_check(dic)
        if name  == "PostgresSQL_config":
            perform_psql_check(dic)
        
        return super().__new__(cls,name,base,dic)


class Checksettings(metaclass=_base):
    """Checks for the imput parameters"""
    pass

def perform_sp_check(dic):
    bac_all_ws = dic.get("backup_all_worksheets")

    if not isinstance(bac_all_ws,bool):
        msg = "backup_all_worksheets should be a Truth value (bool) or not defind"
        raise WrongSettings(msg)
    if (bac_all_ws and dic.get("worksheet_to_consider")) or (not bac_all_ws and not dic.get("worksheet_to_consider")):
        msg = "worksheet_to_consider should be empty if the backup_all_worksheets is True and vice versa"
        raise WrongSettings(msg)
    if not isinstance(dic.get("spreadsheet_name"),str): 
        msg = "spreadsheet_name is not a string or not defined"
        raise WrongSettings(msg)
    if not isinstance(dic.get("credential_path"),str):
        msg = "Invallid path provided"
        raise WrongSettings(msg)
    return True


def perform_psql_check(dic):
    if not "DRIVER" in dic and not isinstance(dic.get("DRIVER"),str):
        msg =  "DRIVER is mandatory and should be a string"
        raise WrongSettings(msg)
    if not "host" in dic and not isinstance(dic.get("host"),str):
        msg =  "host is mandatory and should be a string"
        raise WrongSettings(msg)
    if not "port" in dic and not isinstance(dic.get("port"),int):
        msg =  "port is mandatory and should be a number"
        raise WrongSettings(msg)
    if not "username" in dic and not isinstance(dic.get("username"),str):
        msg =  "username is mandatory and should be a string"
        raise WrongSettings(msg)
    if not "password" in dic and not isinstance(dic.get("password"),str):
        msg =  "password is mandatory and should be a string"
        raise WrongSettings(msg)
    if not isinstance(dic.get("database"),str) and not dic.get('database') == None:
        msg =  "database should be a string or None"
        raise WrongSettings(msg)
    
    return True