import tkinter as tk
import uploader as up # local file uploader.pys


root = tk.Tk()

root.title("Clip Manager by prop")
root.resizable(False, False)

auth = False
uploading = False
channel_name = 'Not Logged In'
video_type = 'Not Logged In'
selected_dir = 'Not Logged In'

# Authentication Function ===============================================================================
def authenticate():

    def submit():
        global auth
        global channel_name
        global video_type
        global selected_dir

        # Getting the client_secrets.json file
        client_secrets = clientSecretsEntry.get()

        # Authenticating the user
        # If the user is authenticated, we will set auth to True
        # and set the channel_name, video_type and selected_dir
        # to the user's preferences
        auth = True
        channel_name = "prop"
        video_type = "mp4"
        selected_dir = "D:\\Editting Stuff Master Version\\Raw Footage\\Valorant"

        # Closing the sub window
        authWindow.destroy()

    global auth
    global channel_name
    global video_type
    global selected_dir

    # We need to retrieve the user's client_id and client_secret
    # from client_secrets.json that the user provides
    # and then use it to authenticate the user
    # if the user is authenticated, we will set auth to True

    # Sub window for authentication (will ask for client_secrets.json)
    authWindow = tk.Toplevel(root)
    authWindow.title("Authentication")

    # Requesting the client_secrets.json file
    clientSecretsLabel = tk.Label(authWindow, text="Please provide the client_secrets.json file")
    clientSecretsLabel.grid(row=0, column=0)

    clientSecretsEntry = tk.Entry(authWindow, width=50)
    clientSecretsEntry.grid(row=1, column=0)

    # Submit Button
    submitButton = tk.Button(authWindow, text="Submit")
    submitButton.grid(row=2, column=0)




# main things go here ===============================================================================

# ---------------------------------------------------------------------------------------------------
# Title of the App
titleFrame = tk.Frame(root)

appNameLabel = tk.Label(titleFrame, text="Clip Manager", font = ("Consolas", 24, "bold"))
appNameLabel.grid(row=0, column=0)
propNameLabel = tk.Label(titleFrame, text="by prop", font = ("Consolas", 20))
propNameLabel.grid(row=1, column=0)

titleFrame.grid(row=0, column=0)

# ---------------------------------------------------------------------------------------------------
# Status Indicator Frame
statusFrame = tk.Frame(root)

# Authenticated Status using coloured text
if auth:
    authStatusLabel = tk.Label(statusFrame, text="Authenticated", fg="green")
else:
    authStatusLabel = tk.Label(statusFrame, text="Not Authenticated", fg="red")
authStatusLabel.grid(row=0, column=0)

# Uploading Status using coloured text
if uploading:
    uploadingStatusLabel = tk.Label(statusFrame, text="Uploading", fg="green")
else:
    uploadingStatusLabel = tk.Label(statusFrame, text="Not Uploading", fg="red")
uploadingStatusLabel.grid(row=1, column=0)

statusFrame.grid(row=0, column=1)


# ---------------------------------------------------------------------------------------------------
# Current Configuration Display Frame
configFrame = tk.Frame(root)

# Current Configuration Display
configLabel = tk.Label(configFrame, text="Current Configuration")
configLabel.grid(row=0, column=0, columnspan=2)

# Labels
authUserLabel = tk.Label(configFrame, text="Authenticated User: ")
authUserLabel.grid(row=1, column=0)
channelNameLabel = tk.Label(configFrame, text="Channel Name: ")
channelNameLabel.grid(row=2, column=0)
videoTypeLabel = tk.Label(configFrame, text="Default Video Type: ")
videoTypeLabel.grid(row=3, column=0)
selectedDirLabel = tk.Label(configFrame, text="Selected Directory: ")
selectedDirLabel.grid(row=4, column=0)

# Authenticated User Display
if auth:
    # Green Text labels next to the label
    authUserLabelValue = tk.Label(configFrame, text=channel_name, fg="green")
    authUserLabelValue.grid(row=1, column=1)
    channelNameLabelValue = tk.Label(configFrame, text=channel_name, fg="green")
    channelNameLabelValue.grid(row=2, column=1)
    videoTypeLabelValue = tk.Label(configFrame, text=video_type, fg="green")
    videoTypeLabelValue.grid(row=3, column=1)
    selectedDirLabelValue = tk.Label(configFrame, text=selected_dir, fg="green")
    selectedDirLabelValue.grid(row=4, column=1)

else:
    # red text labels next to the label
    authUserLabelValue = tk.Label(configFrame, text="None", fg="red")
    authUserLabelValue.grid(row=1, column=1)
    channelNameLabelValue = tk.Label(configFrame, text="None", fg="red")
    channelNameLabelValue.grid(row=2, column=1)
    videoTypeLabelValue = tk.Label(configFrame, text="None", fg="red")
    videoTypeLabelValue.grid(row=3, column=1)
    selectedDirLabelValue = tk.Label(configFrame, text="None", fg="red")
    selectedDirLabelValue.grid(row=3, column=1)
    
configFrame.grid(row=1, column=0, columnspan=2)


# ---------------------------------------------------------------------------------------------------
# Menu Buttons Frame
menuFrame = tk.Frame(root)

# Authenticate Button
if not auth:
    authButton = tk.Button(menuFrame, text="Authenticate", fg="red")
else:
    authButton = tk.Button(menuFrame, text="Authenticate", fg="green")

authButton.grid(row=0, column=0)

# Upload Button
if not uploading:
    uploadButton = tk.Button(menuFrame, text="Upload", fg="red")
else:
    uploadButton = tk.Button(menuFrame, text="Upload", fg="green")

uploadButton.grid(row=1, column=0)

# Options Button
optionsButton = tk.Button(menuFrame, text="Options")
optionsButton.grid(row=2, column=0)

# detailed status button
detailedStatusButton = tk.Button(menuFrame, text="Detailed Status")
detailedStatusButton.grid(row=3, column=0)

# Credits Button
creditsButton = tk.Button(menuFrame, text="Credits")
creditsButton.grid(row=4, column=0)

# Unedittable text box at the bottom showing current upload
uploadTextBox = tk.Entry(menuFrame, width=50, state="readonly")
uploadTextBox.grid(row=5, column=0)


# =============================================================================================
menuFrame.grid(row=2, column=0, columnspan=2)
root.mainloop()