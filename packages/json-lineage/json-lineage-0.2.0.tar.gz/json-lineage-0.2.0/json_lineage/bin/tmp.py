import subprocess


class BinaryReader:
    def __init__(self, binary, fp):
        self.binary = binary
        self.file_path = fp
        self._proc = None


    def ppopen(self):
        self._proc = subprocess.Popen(
            [self.binary, self.file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        # if self._proc.stderr:
        #     err = self._proc.stderr.readlines()

        while True:
            breakpoint()
            line = self._proc.stdout.readline().strip()
            # if self._proc.stderr:
            #     err = self._proc.stderr.readlines()

            if line == "" and self._proc.poll() is not None:
                break
            if line:
                print(line)

        







BinaryReader("./jsonl_converter", "/home/salaah/json-lineage/sample_data/sample.json").ppopen()