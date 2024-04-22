from flask import Flask, request
from datetime import datetime

from pydrive.auth import GoogleAuth
import pydrive
import json
gauth = GoogleAuth()
# Create local webserver and auto handles authentication.
# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")
from pydrive.drive import GoogleDrive

drive = GoogleDrive(gauth)
file_id = "17Q-QRBRn6mPqr9yevNtgUKbnJQXpnmYj"
file_path = "client_secrets.json"
file_temp_path="temp.txt"

def upload_file_to_drive(file_id, local_path):
    """Overwrites the existing Google drive file."""
    update_file = drive.CreateFile({'id': file_id})
    update_file.SetContentFile(local_path)
    update_file.Upload()

def download_drive_file(file_id, save_path):
    """Downloads an existing Google drive file."""
    download_file = drive.CreateFile({'id': file_id})
    download_file.GetContentFile(save_path)  





app = Flask(__name__)

@app.route("/")
def hello():
    return "Helloworld"

@app.route('/upload',methods=['POST'])
def upload_data():
    data= request.json['data']
    print(data)
    
    data=datetime.now().strftime("%d/%m/%Y %H:%M:%S")+","+data+"\n"
    download_drive_file(file_id,file_temp_path)
    with open(file_temp_path, "a") as myfile:
        myfile.write(data  )
    upload_file_to_drive(file_id,file_temp_path)
    return 'Data upload successfully'




if __name__ == '__main__':
    app.run(host='0.0.0.0',port =3000)