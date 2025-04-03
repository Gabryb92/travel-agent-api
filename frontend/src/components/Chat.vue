<template>
  <div class="chat-container">
    <transition-group
      name="message"
      tag="div"
      class="messages"
      ref="messageContainer"
    >
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['message-wrapper', msg.role]"
      >
        <img
          :src="msg.role === 'user' ? userAvatar : assistantAvatar"
          class="avatar"
          :alt="msg.role"
        />
        <div :class="['message-bubble', msg.role]">
          <p v-if="msg.role === 'user'">{{ msg.content }}</p>
          <div
            v-else
            class="assistant-message"
            v-html="marked(msg.content)"
          ></div>
        </div>
      </div>

      <div v-if="loading" key="loading" class="message-wrapper assistant">
        <img :src="assistantAvatar" class="avatar" alt="assistant" />
        <div class="message-bubble assistant">
          <p>Scrivendo...</p>
        </div>
      </div>
    </transition-group>

    <form @submit.prevent="sendMessage" class="input-bar">
      <input
        v-model="newMessage"
        type="text"
        placeholder="Scrivi un messaggio..."
        required
      />
      <button type="submit">Invia</button>
    </form>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { marked } from "marked";

// Importa gli avatar da src/assets
import userAvatar from "../assets/user.png";
import assistantAvatar from "../assets/assistant.png";

const newMessage = ref("");
const messages = ref([
  { role: "assistant", content: "Benvenuto! Come posso aiutarti oggi?" },
]);
const loading = ref(false);
const messageContainer = ref(null);

const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
};

const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  messages.value.push({ role: "user", content: newMessage.value });
  const history = [...messages.value];
  newMessage.value = "";
  loading.value = true;
  scrollToBottom();

  try {
    const res = await fetch("http://127.0.0.1:8080/chat/travel-agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });

    const data = await res.json();

    // Aggiunge solo l’ultimo messaggio AI
    const lastAssistant = [...data].reverse().find((m) => m.type === "ai");
    if (lastAssistant) {
      messages.value.push({
        role: "assistant",
        content: lastAssistant.content,
      });
    }

    // data.forEach((m) => messages.value.push(m)) // backup originale
  } catch (err) {
    messages.value.push({
      role: "assistant",
      content: "Errore nella risposta!",
    });
  } finally {
    loading.value = false;
    scrollToBottom();
  }
};
</script>
