from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, Markdown
from core import graph, config, system_prompt

class TARS(App):

    CSS = """
    #user-input {
        position: relative;
        dock: bottom;
        width: 100%;
        max-width: 100%;
        margin: 1 2 3 4;
        padding: 1 2 3 4;
        background: #1e1e1e;
        border-top: solid #333;
    }
    """

    chat_log: list[dict] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield Markdown("\n".join(f"### **{entry['sender']}:**\n{entry['message']}" for entry in self.chat_log), id="chat_markdown")
        yield Input(placeholder="Enter your message...", id="user_input")
        yield Footer()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        user_message = event.value
        if user_message.strip():
            # Add the user's message to the chat log
            self.chat_log.append({"sender": "You", "message": user_message})

            # Update the Markdown widget with the updated chat log
            markdown_widget = self.query_one("#chat_markdown")
            markdown_widget.update("\n".join(f"### **{entry['sender']}:**\n{entry['message']}" for entry in self.chat_log))

            # Prepare state
            passed_state = {"messages": [{"role": "user", "content": user_message}]}

            # Prepend the system prompt if not already included
            if passed_state["messages"] and passed_state["messages"][0]["role"] != "system":
                passed_state["messages"].insert(0, system_prompt)

            state = {"messages": passed_state["messages"]}

            # Generate response using the graph with persistent memory
            response = graph.invoke(state, config)

            # Extract chatbot response
            chat_response = response["messages"][-1].content

            # Add the bot's response to the chat log
            self.chat_log.append({"sender": "Bot", "message": chat_response})

            # Update the Markdown widget again with the bot's response
            markdown_widget.update("\n".join(f"### **{entry['sender']}:**\n{entry['message']}" for entry in self.chat_log))

            # Reset the input field
            self.query_one("#user_input").value = ""

if __name__ == "__main__":
    TARS().run()
