from pymongo import MongoClient

class Database:
    def __init__(self,hostname,puerto):
        # Conexión a la base de datos
        mongoClient = MongoClient(hostname, puerto)

        # Creamos la base de datos Pulseras
        self.db = mongoClient.pulserasdb

    def get_usuarios(self):
        medicos = self.db.MedicoPacientes;
        output = []
        for q in medicos.find():
            output.append({'Usuario': q['Usuario'], 'PSS': q['PSS']})
        return output

    def get_medicos(self):
        archivos = self.db.MedicoPacientes;
        output = []
        for q in archivos.find():
            output.append({'_idMedico': q['_id'], 'Nombre': q['Nombre'], 'Apellidos': q['Apellidos']})
        return output

    def get_medico(self, idMedico):
        archivos = self.db.MedicoPacientes;
        output = []
        medico = archivos.find({"_id": int(idMedico)})
        for q in medico:
            output.append({'Nombre': q['Nombre'], 'Apellidos': q['Apellidos']})
        return output

    def get_pacientes(self):
        pacientes = self.db.PacientesInformes;
        output = []

        for paciente in pacientes.find():  # 2arrays
            output.append(
                {'_id': int(paciente['_id']),
                 'Nombre': paciente['Nombre'],
                 'Apellidos': paciente['Apellidos'],
                 })
        return output

    def get_paciente(self,idMedico, idPaciente):
        archivos = self.db.MedicoPacientes;
        pacientes = archivos.find_one({"_id": int(idMedico)},
                                      {"Pacientes": {"$elemMatch": {"_idPaciente": int(idPaciente)}}})
        paciente = pacientes['Pacientes'][0]
        return paciente

    ########getIdFiles que me piden ###############
    def get_informes(self,idPaciente):
        print(idPaciente)
        archivos = self.db.PacientesInformes;
        output = []
        informes = archivos.find_one({"_id": int(idPaciente)}, {"Informes": 1})
        print("AQUIiiiiiiii")
        for informe in informes['Informes']:
            output.append(
               {'_idInforme': int(informe['_idInforme']),
                'RutaArchivo': informe['RutaArchivo']})
        return output

    def get_informe(self,idPaciente, idInforme):
        informes = self.db.PacientesInformes.find_one({"_id": float(idPaciente)},
                                                       {"Informes": {"$elemMatch": {"_idInforme": float(idInforme)}}})
        informe = informes['Informes'][0]
        return informe

    def post_informe(self,idPaciente):
        informes = self.db.PacientesInformes.find_one({"_id": int(idPaciente)},
                                                       {"Informes": {"$elemMatch": {"_idInforme": int(idInforme)}}})
        informe = informes['Informes'][0]
        return informe



