import re
import subprocess

startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
startupinfo.wShowWindow = subprocess.SW_HIDE
creationflags = subprocess.CREATE_NO_WINDOW
invisibledict = {
    "startupinfo": startupinfo,
    "creationflags": creationflags,
    "start_new_session": True,
}


def get_all_devices(ffmpegexe: str) -> dict:
    r"""
    Retrieves information about all available video and audio devices using FFmpeg.

    Args:
        ffmpegexe (str): The path to the FFmpeg executable.

    Returns:
        dict: A dictionary containing information about all available devices.
              The dictionary has two keys: "video" and "audio".
              The value of each key is another dictionary where the keys are device names
              and the values are device identifiers.

    Example:
        from ffmpegdevices import get_all_devices
        ffmpegexe = r"C:\ffmpeg\ffmpeg.exe"
        devices = get_all_devices(ffmpegexe)
        print(devices)
        {
            "video": {
                "HD Pro Webcam C920": "@device_pnp_\\\\?\\xxxxxxxxxxxxxxxxxx\\global",
                "Logi Capture": "@device_sw_{8xxxxxxxxxxxxxxxxxxxxxxx6}\\{4xxxxxxxxxxxxxxA}",
                "OBS Virtual Camera": "@device_sw_{xxxxxxxxxxxxxxxxx1CE86}\\{A3FxxxxxxxxxxxxxxxxxxEC20B}",
            },
            "audio": {
                "Krisp Microphone (Krisp Audio)": "@device_cm_{33xxxxxxxxxxxxxxxxE86}\\wave_{7xxxxxxxxxxxxxxxx9FC58}",
                "Microphone (2- USB Advanced Audio Device)": "@device_cm_{3xxxxxxxxxxx86}\\wave_{Fxxxxxxxxxxxxxxxxxxxxxxxxx7C65BED9}",
            },
        }
    """
    p = subprocess.run(
        [ffmpegexe, "-list_devices", "true", "-f", "dshow", "-i", "dummy"],
        capture_output=True,
        **invisibledict,
    )
    alldevices = {}

    for d in [
        (q[1][1:-1].decode("utf-8"), q[0].decode("utf-8"), q[-1].decode("utf-8"))
        for q in [
            re.findall(
                rb'("([^"]+)"[^"]+(\([^\)]+\))[^"]+"([^"]+)")',
                x.replace(b"\n", b" ").replace(b"\r", b" "),
            )[0][1:]
            for x in re.findall(
                rb'(\[[^\]]+\][^\n\r]+\([^\)]+\)[\r\n]+.*?Alternative name\s+"[^\r\n]+)',
                p.stderr,
                flags=re.DOTALL,
            )
        ]
    ]:
        if d[0] not in alldevices:
            alldevices[d[0]] = {}
        alldevices[d[0]][d[1]] = d[2]

    return alldevices

