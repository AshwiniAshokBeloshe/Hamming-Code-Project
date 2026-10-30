
from pyscript import document


def process_data(event):
    data = document.querySelector("#data").value.strip()
    output = document.querySelector("#output")
    position = int(
        document.querySelector("#error_pos").value
    )

    # Validate binary input
    if len(data) != 4 or any(b not in "01" for b in data):
        output.innerHTML = (
            "<span style='color:red'>"
            "Enter exactly 4 binary bits (0 or 1)."
            "</span>"
        )
        return

    # Create Hamming code
    code = [0] * 8

    code[3] = int(data[0])
    code[5] = int(data[1])
    code[6] = int(data[2])
    code[7] = int(data[3])

    # Calculate even parity bits
    code[1] = code[3] ^ code[5] ^ code[7]
    code[2] = code[3] ^ code[6] ^ code[7]
    code[4] = code[5] ^ code[6] ^ code[7]

    generated = ''.join(str(x) for x in code[1:])

    # Simulate transmission error
    if position != 0:
        code[position] ^= 1

    received = ''.join(str(x) for x in code[1:])

    # Check parity bits
    s1 = code[1] ^ code[3] ^ code[5] ^ code[7]
    s2 = code[2] ^ code[3] ^ code[6] ^ code[7]
    s4 = code[4] ^ code[5] ^ code[6] ^ code[7]

    error = s1 + 2 * s2 + 4 * s4

    # Correct single-bit error
    if error != 0:
        code[error] ^= 1

    corrected = ''.join(str(x) for x in code[1:])

    recovered = ''.join(
        str(code[i]) for i in [3, 5, 6, 7]
    )

    if error == 0:
        status = (
            "<span class='success'>"
            "No error detected."
            "</span>"
        )
    else:
        status = (
            f"Error detected at bit position {error}.<br>"
            "<span class='success'>"
            "Single-bit error corrected!"
            "</span>"
        )

    # Display results
    output.innerHTML = (
        f"<b>Original Data:</b> {data}<br>"
        f"<b>Generated Hamming Code:</b> {generated}<br>"
        f"<b>Received Code:</b> {received}<br>"
        f"<b>Status:</b> {status}<br>"
        f"<b>Corrected Code:</b> {corrected}<br>"
        f"<b>Recovered Data:</b> {recovered}"
    )
