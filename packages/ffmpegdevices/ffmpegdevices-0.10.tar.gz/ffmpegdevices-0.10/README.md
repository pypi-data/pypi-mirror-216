# Retrieves information about all available video and audio devices using FFmpeg.

## pip install ffmpegdevices

#### Tested against Windows 10 / Python 3.10 / Anaconda

```python

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


```