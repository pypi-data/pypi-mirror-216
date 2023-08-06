import serial
import time

class Synchro:
    def __init__(self, port:int) -> None:
        self.ser = serial.Serial()
        self.ser.baudrate = 19200
        self.ser.timeout = 2.0
        self.ser.port = f"COM{port}"
    
    def open(self) -> bool:
        try:
            self.ser.open()
            time.sleep(1.5)
            return True
        except serial.SerialException as e:
            print(e)
            return False

    def close(self) -> None:
        self.ser.close()

    def selfIsReady(self) -> None:
        self.ser.write(b"READY")
    
    def waitSync(self) -> bool:
        return self.ser.readline().decode("Ascii").strip() == "SYNCED"
    
    def unsync(self) -> None:
        self.ser.write(b"UNSYNC")
    
    def unsync(self) -> None:
        self.ser.write(b"RESYNC")
    
    def start(self) -> None:
        self.ser.reset_input_buffer()
        self.ser.reset_output_buffer()

        self.ser.write(b"START")
    
    def finished(self) -> None:
        self.ser.write(b"FINISH")
