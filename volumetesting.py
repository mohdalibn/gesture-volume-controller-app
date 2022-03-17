# library and its flies for controlling the volume
import pycaw
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initializations from the pycaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

#volume.GetMute()
#volume.GetMasterVolumeLevel()
VolumeRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)


MinVolume = VolumeRange[0]
print(MinVolume)

