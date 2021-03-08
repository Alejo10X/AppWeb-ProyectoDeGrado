import time
import calendar
from datetime import datetime


def generateFileName(channelID):
    filename = 'CloudData_' + channelID + '_' + str(calendar.timegm(time.gmtime())) + '.csv'

    return filename

def uploadFileTime():
    fileTime = datetime.now().strftime('%d/%m/%Y %X').rsplit(' ')

    return fileTime[0], fileTime[1]


def groupFileData(filename, filetype, origin, date, time, url):
    filedata = {
        'filename': filename,
        'filetype': filetype,
        'origin': origin,
        'date': date,
        'time': time,
        'url': url
    }

    return filedata


# def allowed_file(filename):
#     # ARCHIVOS PERMITIDOS
#     # Retorna TRUE si el archivo posee '.' en la extensión del archivo y si la extensión exsiste en la lista de extensiones permitidas 

#     return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



# def allowed_divs(userheaders):
#     # DIVISORES PERMITIDOS
#     # Obtiene la lista de headers que ingresa el usuario y los separa de acuerdo con la lista de divisores permitidos, al final retorna una nueva lista con los nombres de las cabeceras separadas.

#     for divider in ALLOWED_DIVIDERS:
#         if divider in userheaders:
#             finalheaders = userheaders.split(divider)
    
#     return finalheaders



# def split_fileinfo(filename):
#     # INFORMACIÓN DEL ARCHIVO
#     # Obtiene el nombre del archivo y retorna una lista con el nombre y la extensión del archivo por separado.

#     fileinfo = [filename.rsplit('.', 1)[0], filename.rsplit('.', 1)[1]] 
#     return fileinfo



# def rename_file(extension):
#     # RENOMBRAR ARCHIVO
#     # Obtiene la fecha y la hora en la cual se subió al archivo al servidor
#     # y le agrega la extensión original, para renombrar el archivo.

#     fixdate = datetime.datetime.now().strftime('%x %X')
#     newfilename = secure_filename('ServerFile_'+fixdate+'.'+extension)
#     return newfilename



# def just_rename(filename, extension):
#     new_filename = filename +'.'+ extension
#     return new_filename



def determineFileType(filename):

    extension = filename.rsplit('.', 1)[1]

    if extension == 'csv':
        filetype = ('Valores separados por comas')

    elif extension == 'xlsx' or extension == 'xls':
        filetype = ('Archivo de Microsoft Excel')
    
    elif extension == 'ods':
        filetype = ('Archivo de OpenDocument')

    return filetype