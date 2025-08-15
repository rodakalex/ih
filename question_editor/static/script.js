let questions = [];
let index = 0;
let isDirty = false;

const questionEl = document.getElementById("question");
const statusEl = document.getElementById("status");

// Подключаем CodeMirror для answer
const answerEditor = CodeMirror.fromTextArea(document.getElementById("answer"), {
    mode: "htmlmixed",
    lineNumbers: true,
    theme: "default"
});
answerEditor.on("change", markChanged);

questionEl.addEventListener("input", markChanged);

function getIdFromURL() {
    // поддержим и /q/123, и ?id=123
    const m = window.location.pathname.match(/^\/q\/(\d+)/);
    if (m) return parseInt(m[1], 10);
    const p = new URLSearchParams(window.location.search).get("id");
    return p ? parseInt(p, 10) : null;
}

async function load() {
    const res = await fetch("/api/questions");
    questions = await res.json();

    // выбрать позицию по id из URL (если есть)
    const idFromURL = getIdFromURL();
    if (idFromURL) {
        const i = questions.findIndex(q => q.id === idFromURL);
        if (i !== -1) index = i;
    }

    show();
}

function markChanged() {
    if (!isDirty) {
        isDirty = true;
        statusEl.textContent = "✏️ Изменено";
    }
}

function show() {
    if (questions.length === 0) {
        questionEl.value = "Нет вопросов";
        answerEditor.setValue("");
        statusEl.textContent = "";
        // сбросим URL если пусто
        if (window.location.pathname.startsWith("/q/")) {
            history.replaceState(null, "", "/");
        }
        return;
    }

    index = Math.max(0, Math.min(index, questions.length - 1));
    const q = questions[index];

    questionEl.value = q.question || "";
    answerEditor.setValue(q.answer || "");

    // 🔥 вот эта часть — обновление URL
    const newPath = `/q/${q.id}`;
    if (window.location.pathname !== newPath) {
        history.replaceState(null, "", newPath);
    }

    isDirty = false;
    statusEl.textContent = "";
}

async function save() {
    const q = questions[index];
    const form = new FormData();
    form.append("id", q.id);
    form.append("question", questionEl.value);
    form.append("answer", answerEditor.getValue());

    await fetch("/api/update", { method: "POST", body: form });
    q.question = questionEl.value;
    q.answer = answerEditor.getValue();
    isDirty = false;
    statusEl.textContent = "✅ Сохранено";
}
async function del() {
    if (!confirm("Удалить этот вопрос?")) return;

    const q = questions[index];
    const form = new FormData();
    form.append("id", q.id);

    await fetch("/api/delete", { method: "POST", body: form });

    // Удаляем из массива и показываем соседний
    questions.splice(index, 1);
    if (index >= questions.length) index = Math.max(0, questions.length - 1);
    show();
}

function next() {
    if (index + 1 < questions.length) {
        index++;
        show();
    }
}

function prev() {
    if (index > 0) {
        index--;
        show();
    }
}

load();