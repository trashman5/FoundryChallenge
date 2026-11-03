import os
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

ENDPOINT = "https://foundry-tecnun-resource.services.ai.azure.com/api/projects/foundry-tecnun-project"
AGENT_NAME = "my-agent"  # put your real agent name here
EXIT_WORDS = {"exit", "quit", "salir"}


def save_generated_files(openai_client, response):
    """Download files made by Code Interpreter (e.g. charts) into the current folder."""
    for item in response.output:
        if item.type != "message":
            continue
        for part in item.content:
            for ann in getattr(part, "annotations", None) or []:
                if ann.type == "container_file_citation":
                    data = openai_client.containers.files.content.retrieve(
                        file_id=ann.file_id, container_id=ann.container_id
                    )
                    filename = os.path.basename(ann.filename)
                    with open(filename, "wb") as f:
                        f.write(data.read())
                    print(f"[saved file: {filename}]")


def main():
    with (
        DefaultAzureCredential() as credential,
        AIProjectClient(
            endpoint=ENDPOINT,
            credential=credential,
            allow_preview=True,
        ) as project_client,
    ):
        openai_client = project_client.get_openai_client(agent_name=AGENT_NAME)

        # One conversation for the whole session, so the agent keeps the context.
        conversation = openai_client.conversations.create()
        print(f"Connected to '{AGENT_NAME}'. Type 'exit' to quit.\n")

        while True:
            try:
                user_message = input("You: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nBye!")
                break

            if not user_message:
                continue
            if user_message.lower() in EXIT_WORDS:
                print("Bye!")
                break

            try:
                response = openai_client.responses.create(
                    conversation=conversation.id,
                    input=[{"role": "user", "content": user_message}],
                )
            except Exception as e:  # keep the session alive on a failed request
                print(f"[error] {e}\n")
                continue

            print(f"\nAgent: {response.output_text}\n")
            save_generated_files(openai_client, response)


if __name__ == "__main__":
    main()