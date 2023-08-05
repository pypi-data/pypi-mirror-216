import argparse


def main(args=None):
    parser = argparse.ArgumentParser(
        description="Express Env CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.parse_args(args=args)


if __name__ == "__main__":
    main()
