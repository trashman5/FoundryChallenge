import os
import streamlit as st
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

ENDPOINT = "https://foundry-tecnun-resource.services.ai.azure.com/api/projects/foundry-tecnun-project"
AGENT_NAME = "my-agent"  # put your real agent name here

st.set_page_config(page_title="Study Coach", page_icon="🟢")
st.title("CF-101 Study Coach")


@st.cache_resource
def get_clients():
    """Created once and shared by all sessions. Keep both objects alive."""
    credential = DefaultAzureCredential()
    project_client = AIProjectClient(
        endpoint=ENDPOINT, credential=credential, allow_preview=True
    )
    return project_client, project_client.get_openai_client(agent_name=AGENT_NAME)


_project_client, client = get_clients()


def new_conversation():
    st.session_state.conversation_id = client.conversations.create().id
    st.session_state.messages = []  # each: {"role", "content", "files"}


def extract_files(response):
    """Download files created by Code Interpreter (charts, etc.)."""
    files = []
    for item in response.output:
        if item.type != "message":
            continue
        for part in item.content:
            for ann in getattr(part, "annotations", None) or []:
                if ann.type == "container_file_citation":
                    data = client.containers.files.content.retrieve(
                        file_id=ann.file_id, container_id=ann.container_id
                    )
                    files.append((os.path.basename(ann.filename), data.read()))
    return files


def show_files(files, key_prefix):
    for i, (name, data) in enumerate(files):
        if name.lower().endswith((".png", ".jpg", ".jpeg")):
            st.image(data, caption=name)
        else:
            st.download_button(f"Download {name}", data, file_name=name,
                               key=f"{key_prefix}-{i}")


if "conversation_id" not in st.session_state:
    new_conversation()

with st.sidebar:
    st.write(f"Agent: `{AGENT_NAME}`")
    if st.button("New conversation"):
        new_conversation()
        st.rerun()

# Replay the history (Streamlit reruns the script on every interaction).
for n, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        show_files(msg["files"], key_prefix=f"hist-{n}")

if prompt := st.chat_input("Ask your study coach..."):
    st.session_state.messages.append({"role": "user", "content": prompt, "files": []})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            with st.spinner("Meditating..."):
                response = client.responses.create(
                    conversation=st.session_state.conversation_id,
                    input=[{"role": "user", "content": prompt}],
                )
                answer = response.output_text
                files = extract_files(response)
        except Exception as e:
            answer, files = f"Error: {e}", []
        st.markdown(answer)
        show_files(files, key_prefix="new")

    st.session_state.messages.append(
        {"role": "assistant", "content": answer, "files": files}
    )