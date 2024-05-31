# import wave package to read and write .wav audio file
import wave
path_to_audio_file = "audio/alvin.wav"
path_to_text_file = "text/text.txt"
path_to_save_new_audio_file_to = "audio/audio_embedded.wav"


def check_length(n_bits_that_can_be_encoded, n_bits_to_encode):
    if n_bits_that_can_be_encoded - n_bits_to_encode < 0:
        print("Carrier Signal does not carry enough samples to encode secret text.")
        print("Number of bits that can be encoded in the audio file:", n_bits_that_can_be_encoded)
        print("Number of bits in the secret text provided:", n_bits_to_encode)
        print("Choose a larger audio file or a smaller text.")
        exit(1)


def append_dummy_chars_to_text(text, bytes_from_carrier, dummy_char):
    n_bits_to_encode = len(text) * 8
    n_bytes = len(bytes_from_carrier)
    # can encode one bit per n_bytes_per_sample bytes (3 bytes at 24 bit bit-depth)
    n_bits_that_can_be_encoded = n_bytes // n_bytes_per_sample
    # one ASCII dummy char needs 8 bits to be saved
    check_length(n_bits_that_can_be_encoded, n_bits_to_encode)
    n_dummy_chars = (n_bits_that_can_be_encoded - n_bits_to_encode) // 8
    return text + n_dummy_chars * dummy_char


def embed_secret_into_carrier(secret_bits_list, carrier_bytes):
    secret_bit_index = 0
    for carrier_byte_index in range(0, len(carrier_bytes)):
        if secret_bit_index < len(secret_bits_list):
            current_bit = secret_bits_list[secret_bit_index]
            # first byte is always the leas significant byte of the sample
            if carrier_byte_index % n_bytes_per_sample == 0:
                # first: logical AND with 254 (0b11111110)
                # second: logical OR with current_bit
                carrier_bytes[carrier_byte_index] = (carrier_bytes[carrier_byte_index] & 254) | current_bit
                secret_bit_index += 1
        else:
            break
    return bytes(carrier_bytes)


# wave.open returns a Wave_read object
# mode: read bytes
carrier_audio = wave.open(path_to_audio_file, mode='rb')
print(carrier_audio.getparams())
# sample width = bit depth in bytes: how many bytes per sample of audio
n_bytes_per_sample = carrier_audio.getsampwidth()
# all bytes from all frames as bytearray (mutable!)
carrier_bytes = bytearray(carrier_audio.readframes(carrier_audio.getnframes()))

with open(path_to_text_file, 'r') as f:
    secret_text = ascii(f.read())


secret_text = append_dummy_chars_to_text(secret_text, carrier_bytes, '@')
print(secret_text)

# return a list of bytes from the string: format each character to bit representation with a leading 0 (to make bytes)
bytes_from_secret_string = [format(ord(char), '08b') for char in secret_text]
secret_bits_list = [int(bit) for char in secret_text for bit in format(ord(char), '08b')]

# do we have as many bytes // n_bytes_per_sample in the carrier as bits in the secret?
# print(len(carrier_bytes) // n_bytes_per_sample, len(secret_bits_list))

carrier_bytes = embed_secret_into_carrier(secret_bits_list, carrier_bytes)
with wave.open(path_to_save_new_audio_file_to, 'wb') as fd:
    fd.setparams(carrier_audio.getparams())
    fd.writeframes(carrier_bytes)
carrier_audio.close()
