<template>
  <div class="chat-container">
    <div class="messages" ref="messageContainer">
      <transition-group name="message" tag="div">
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
    </div>

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
import { ref, nextTick, watch, onMounted } from "vue"; // Riaggiunto onMounted se non c'era
import { marked } from "marked";

import userAvatar from "../assets/user.png";
import assistantAvatar from "../assets/assistant.png";

const newMessage = ref("");
const messages = ref([
  { role: "assistant", content: "Benvenuto! Come posso aiutarti oggi?" },
]);
const loading = ref(false);
const messageContainer = ref(null); // Il tuo ref originale sul div .messages

// La tua funzione scrollToBottom originale con nextTick
const scrollToBottom = () => {
  nextTick(() => {
    // messageContainer.value dovrebbe essere l'elemento DOM div.messages
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
};

// Lasciamo i watcher originali, potrebbero essere utili come fallback
// ma le chiamate esplicite sono più affidabili in questo caso.
watch(messages, scrollToBottom, { deep: true }); // Aggiungi deep: true per sicurezza
watch(loading, scrollToBottom);

// LA TUA FUNZIONE sendMessage ORIGINALE
// con aggiunta ESCLUSIVA di chiamate a scrollToBottom()
const sendMessage = async () => {
  if (!newMessage.value.trim()) return;

  // 1. Aggiungi messaggio utente
  messages.value.push({ role: "user", content: newMessage.value });
  const history = [...messages.value]; // La tua logica per history
  newMessage.value = "";
  // *** CHIAMA SCROLL QUI *** dopo aver aggiunto il messaggio utente
  scrollToBottom();

  // 2. Imposta loading
  loading.value = true;
  // Potremmo chiamare scrollToBottom() anche qui se lo stato "Scrivendo..."
  // causa problemi di scroll, ma di solito non è necessario.
  // Prova senza prima, se serve aggiungi: scrollToBottom();

  try {
    const res = await fetch("http://127.0.0.1:8080/chat/travel-agent", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });

    // Aggiungiamo un controllo base sull'ok della risposta, senza cambiare la logica
    if (!res.ok) {
      console.error("Errore HTTP:", res.status, await res.text()); // Logga l'errore
      throw new Error("Errore HTTP"); // Lancia errore per andare al catch
    }

    const data = await res.json(); // La tua gestione della risposta

    // La tua logica originale per trovare il messaggio dell'assistente
    // ASSUMO CHE la risposta `data` sia l'array COMPLETO dei messaggi
    // e che il messaggio assistente abbia `type: 'ai'` come nella tua prima versione implicita.
    // SE la struttura è diversa (es. `role: 'assistant'`), modifica il `.find` qui sotto.
    const lastAssistant = [...data].reverse().find((m) => m.type === "ai"); // MODIFICA type/ai SE NECESSARIO

    if (lastAssistant) {
      // 3. Aggiungi messaggio assistente
      messages.value.push({
        role: "assistant", // Frontend usa 'role'
        content: lastAssistant.content,
      });
      // *** CHIAMA SCROLL QUI *** dopo aver aggiunto il messaggio assistente
      scrollToBottom();
    } else {
      // Potresti voler gestire il caso in cui non trovi 'lastAssistant'
      console.warn("Nessun messaggio 'ai' trovato nella risposta:", data);
    }
  } catch (err) {
    // 4. Gestione errore (la tua logica originale)
    messages.value.push({
      role: "assistant",
      content: "Errore nella risposta!",
    });
    // *** CHIAMA SCROLL QUI *** dopo aver aggiunto il messaggio di errore
    scrollToBottom();
    // Logghiamo anche l'errore per debug nel browser console
    console.error("Errore durante sendMessage:", err);
  } finally {
    // 5. Rimuovi loading
    loading.value = false;
    // Chiamiamo lo scroll anche qui, perché rimuovere "Scrivendo..." cambia l'altezza
    scrollToBottom();
  }
};

// Scroll iniziale quando il componente è montato
onMounted(() => {
  scrollToBottom();
});
</script>
