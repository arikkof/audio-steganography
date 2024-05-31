import wave
path_to_audio_file = "audio/audio_embedded.wav"
file_to_write_to = "text/extracted_secret_text.txt"


def extract_lsb_bits(audio_bytes):
    bits = []
    for i, byte in enumerate(audio_bytes):
        # first byte of the sample is least significant byte
        if i % n_bytes_per_sample == 0:
            # append least significant bit of the current byte to the array
            bits.append(byte & 1)
    return bits


def make_bytes_from_bits(bits):
    # append 0s if cannot make full bytes from all bits
    if len(bits) % 8 != 0:
        bits += [0] * (8 - len(bits) % 8)
    # fasse 8 bits zu einem byte zusammen
    bytes = []
    for i in range(0, len(bits), 8):
        byte_bits = bits[i:i + 8]
        byte = 0
        for bit in byte_bits:
            byte = (byte << 1) | bit
        bytes.append(byte)
    return bytes


def make_string_from_bytes(secret_bytes):
    string = ""
    for byte in secret_bytes:
        string += chr(byte)
    return string


audio = wave.open(path_to_audio_file, mode='rb')
print(audio.getparams())
bytes_from_audio = bytearray(audio.readframes(audio.getnframes()))
n_bytes_per_sample = audio.getsampwidth()

extracted_secret_bits = extract_lsb_bits(bytes_from_audio)

extracted_secret_bytes = make_bytes_from_bits(extracted_secret_bits)

extracted_secret_string = make_string_from_bytes(extracted_secret_bytes)

text_file = open(file_to_write_to, "w")
text_file.write(extracted_secret_string)
text_file.close()

print(extracted_secret_string)
