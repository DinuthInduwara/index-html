import subprocess, re, os
from datetime import date


def rclone_Upload(path, message):
    today = date.today()
    d2 = today.strftime("%B %d %Y")

    conf_path= './downloads/rclone.conf'
    dest_drive = "unlimited"


    rclone_copy_cmd = [
        "rclone",
        "copy",
        f"--config={conf_path}",
        str(path),
        f"{dest_drive}:{today.strftime('%Y')}/{d2}",
        "-f",
        "- *.!qB",
        "--buffer-size=1M",
        "-P",
    ]

    rclone_pr = subprocess.Popen(rclone_copy_cmd, stdout=subprocess.PIPE)
    rcres = rclone_process_display(rclone_pr, message, path)



def rclone_process_display(process, message, path):
    blank = 0
    sleeps = False
    while True:

        data = process.stdout.readline().decode()
        data = data.strip()
        mat = re.findall(r"Transferred:.*ETA.*", data)

        if mat is not None:
            if len(mat) > 0:
                sleeps = True
                try:message.edit(mat)
                except:pass


        if data == "":
            blank += 1
            if blank <= 20:
                break
        else:
            blank = 0

        if sleeps:
            sleeps = False
            process.stdout.flush()
    os.remove(path)


    





