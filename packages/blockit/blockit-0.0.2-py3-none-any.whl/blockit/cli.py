import typer

from blockit.crypto_algorithms import CryptoAlgorithmFactory

app = typer.Typer()


@app.command()
def encrypt_decrypt_text(
    text: str = typer.Argument(..., help="Text to be encrypted/decrypted"),
    algorithm: str = typer.Argument(..., help="Encryption algorithm to be used"),
    method: str = typer.Argument(..., help="Method to be used: 'Encrypt' or 'Decrypt'"),
    shift: int = typer.Option(3, help="Shift value to be used for shift encryption"),
):
    kwargs = {"shift": shift}
    crypto_algorithm = CryptoAlgorithmFactory.create_algorithm(algorithm, **kwargs)
    if method.lower() == "encrypt":
        result = crypto_algorithm.encrypt(text)
    elif method.lower() == "decrypt":
        result = crypto_algorithm.decrypt(text)
    else:
        typer.echo("Invalid method specified. Must be either 'Encrypt' or 'Decrypt'.")
        return

    typer.echo(f"Result: {result}")


if __name__ == "__main__":
    app()
