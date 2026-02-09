import argparse
from src.ingestion.ingestor import DocumentIngestor
from src.vector_db.store_fabric import create_vector_store


def main():
    parser = argparse.ArgumentParser(description="Document Manager")
    parser.add_argument("command", choices=["add", "delete", "update"], help="Operation to perform")
    parser.add_argument("paths", nargs="+", help="Paths to documents")

    args = parser.parse_args()
    store = create_vector_store()
    ingestor = DocumentIngestor(store=store)

    if args.command == "add":
        ingestor.add_files(args.paths)
        print(f"Added files: {args.paths}")
    elif args.command == "delete":
        ingestor.delete_files(args.paths)
        print(f"Deleted files: {args.paths}")
    elif args.command == "update":
        ingestor.update_files(args.paths)
        print(f"Updated files: {args.paths}")

if __name__ == "__main__":
    main()
