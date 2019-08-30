from pymongo import MongoClient

class Database:
    def __init__(self,hostname,puerto):
        # Conexión a la base de datos
        mongoClient = MongoClient(hostname, puerto)

        # Creamos la base de datos Pulseras
        self.db = mongoClient.pulserasdb

    def get_medicos(self):
        archivos = self.db.archivos;
        output = []
        for q in archivos.find():
            output.append({'_idMedico': q['_id'], 'Nombre': q['Nombre'], 'Apellidos': q['Apellidos']})
        return output

    def get_medico(self, idMedico):
        archivos = self.db.archivos;
        output = []
        medico = archivos.find({"_id": int(idMedico)})
        for q in medico:
            output.append({'Nombre': q['Nombre'], 'Apellidos': q['Apellidos']})
        return output

    def get_pacientes(self, idMedico):
        pacientes = self.db.archivos;
        output = []
        pacientes = pacientes.find_one({"_id": int(idMedico)}, {"Pacientes": 1})

        for paciente in pacientes['Pacientes']:  # 2arrays
            output.append(
                {'_idPaciente': paciente['_idPaciente'],
                 'Nombre': paciente['Nombre'],
                 'Apellidos': paciente['Apellidos'],
                 })
        return output

    def get_pacientes2(self):
        pacientes = self.db.PacientesInformes;
        output = []

        for paciente in pacientes.find():  # 2arrays
            output.append(
                {'_id': paciente['_id'],
                 'Nombre': paciente['Nombre'],
                 'Apellidos': paciente['Apellidos'],
                 })
        return output

    def get_paciente(self,idMedico, idPaciente):
        archivos = self.db.archivos;
        pacientes = archivos.find_one({"_id": int(idMedico)},
                                      {"Pacientes": {"$elemMatch": {"_idPaciente": int(idPaciente)}}})
        paciente = pacientes['Pacientes'][0]
        return paciente

    ########getIdFiles que me piden ###############
    def get_informes(self,idPaciente):
        archivos = self.db.PacientesInformes;
        output = []
        informes = archivos.find_one({"_id": int(idPaciente)}, {"Informes": 1})
        for informe in informes['Informes']:
            output.append(
               {'_idInforme': informe['_idInforme'],
                'RutaArchivo': informe['RutaArchivo']})
        return output

    def get_informe(self,idPaciente, idInforme):
        informes = self.db.PacientesInformes.find_one({"_id": int(idPaciente)},
                                                       {"Informes": {"$elemMatch": {"_idInforme": int(idInforme)}}})
        informe = informes['Informes'][0]
        return informe

    def post_informe(self,idPaciente):
        informes = self.db.PacientesInformes.find_one({"_id": int(idPaciente)},
                                                       {"Informes": {"$elemMatch": {"_idInforme": int(idInforme)}}})
        informe = informes['Informes'][0]
        return informe



