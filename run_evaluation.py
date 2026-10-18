from dataset import validate_dataset

def main():
    try:
        validate_dataset()
        print("Dataset validation passed.")
    except ValueError as error:
        print(f"Dataset incomplete: {error}")

if __name__ == "__main__":
    main()
