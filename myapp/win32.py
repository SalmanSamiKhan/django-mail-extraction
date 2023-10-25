import win32com.client
import os
import pandas as pd

def get_mails():
    # Connect to Outlook
    outlook = win32com.client.Dispatch("Outlook.Application")
    namespace = outlook.GetNamespace("MAPI")

    # Create output folder
    root_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(root_dir, "Output Mails")

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # folder_name = 'salman@altersenseltd.onmicrosoft.com'
    folder_name = "salman@altersenseltd.onmicrosoft.com"

    # Find the folder by name
    target_folder = None
    for folder in namespace.Folders:
        if folder.Name.lower() == folder_name.lower():
            target_folder = folder
            break

    if target_folder is not None:
        # Iterate through the folders within the target folder

        for folder in target_folder.Folders:
            local_folder_path = os.path.join(output_dir, folder.Name)
            if not os.path.exists(local_folder_path):
                os.makedirs(local_folder_path)

            csv_data = {
                "MSGID": [],
                "FROM": [],
                "TO": [],
                "CC": [],
                "SUBJECT": [],
                "EMAIL BODY": [],
                "DATE SENT": [],
                "DATE RECEIVED": [],
                "PATH": [],
            }

            for message in folder.Items:
                pst_path = os.path.join(local_folder_path, f"{message.EntryID[-30:]}.pst")
                message.SaveAs(pst_path)

                csv_data["MSGID"].append(message.EntryID)
                csv_data["DATE SENT"].append(
                    message.SentOn.strftime("%Y-%m-%d %H:%M:%S %z")
                )
                csv_data["DATE RECEIVED"].append(
                    message.ReceivedTime.strftime("%Y-%m-%d %H:%M:%S %z")
                )
                csv_data["FROM"].append(message.SenderName)
                csv_data["TO"].append(message.To)
                csv_data["CC"].append(message.CC)
                csv_data["SUBJECT"].append(message.Subject)
                csv_data["EMAIL BODY"].append(message.Body)
                csv_data["PATH"].append(f"{local_folder_path}/{message.EntryID[-30:]}.pst")

            df = pd.DataFrame(csv_data)
            csv_file_path = os.path.join(local_folder_path, f"{folder.Name}.csv")
            if not df.empty:
                df.to_csv(csv_file_path, index=False)