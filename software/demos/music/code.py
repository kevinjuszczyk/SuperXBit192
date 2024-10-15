import board
import digitalio
import pwmio
import time

sel = digitalio.DigitalInOut(board.GP28)
sel.pull = digitalio.Pull.UP
sel.direction = digitalio.Direction.INPUT

#https://blog.wokwi.com/play-musical-notes-on-circuitpython/
def note(name):
    octave = int(name[-1])
    PITCHES = "c,c#,d,d#,e,f,f#,g,g#,a,a#,b".split(",")
    pitch = PITCHES.index(name[:-1].lower())
    return int(440 * 2 ** ((octave - 4) + (pitch - 9) / 12.))

rowyourboat = [
  ("g5", 48), ("g5", 48), ("g5", 36), ("a5", 12), ("b5", 48),
  ("b5", 36), ("a5", 12), ("b5", 36), ("c6", 12), ("d6", 96),
  ("g6", 16), ("g6", 16), ("g6", 16), ("d6", 16), ("d6", 16), ("d6", 16),
  ("b5", 16), ("b5", 16), ("b5", 16), ("g5", 16), ("g5", 16), ("g5", 16),
  ("d6", 36), ("c6", 12), ("b5", 36), ("a5", 12), ("g5", 96)
]

korobeiniki = [
    ("e5", 48), ("b4", 24), ("c5", 24), ("d5", 48), ("c5", 24), ("b4", 24), ("a4", 48),
    ("a4", 24), ("c5", 24), ("e5", 48), ("d5", 24), ("c5", 24), ("b4", 48), ("b4", 48),
    ("c5", 48), ("d5", 48), ("e5", 48), ("c5", 48), ("a4", 48), ("a4", 48),
    ("d5", 48), ("f5", 24), ("a5", 24), ("g5", 48), ("f5", 24), ("e5", 24), ("d5", 48),
    ("e5", 24), ("c5", 24), ("e5", 48), ("d5", 24), ("c5", 24), ("b4", 48), ("b4", 48),
    ("c5", 48), ("d5", 48), ("e5", 48), ("c5", 48), ("a4", 48), ("a4", 48)
]

while True:
    if sel.value == False:
        for (notename, one92nds) in korobeiniki:
            length = one92nds * 0.01
            if notename:
                buzzer = pwmio.PWMOut(board.GP20,frequency=note(notename))
                buzzer.duty_cycle = 2 ** 14 #25% duty cycle seems louder than 50%
            time.sleep(length)
            buzzer.deinit()
    else:
        time.sleep(0.1)