function el(id) {
  return document.getElementById(id);
}

function esc(value) {
  var d = document.createElement("div");
  d.textContent = value === null || value === undefined ? "" : String(value);
  return d.innerHTML;
}

function loading(box) {
  box.innerHTML = '<span class="loading">Thinking... please wait</span>';
}

async function postJSON(url, payload) {
  var res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  return await res.json();
}

function bindSimple(formId, inputId, boxId, url, keyName, label, pickField) {
  var form = el(formId);
  if (!form) return;

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    var value = el(inputId).value.trim();
    if (!value) return;

    var box = el(boxId);
    var btn = form.querySelector("button");
    btn.disabled = true;
    loading(box);

    try {
      var payload = {};
      payload[keyName] = value;
      var data = await postJSON(url, payload);
      var out = data[pickField] || data.error || JSON.stringify(data);
      box.innerHTML = "<b>" + label + "</b>\n\n" + esc(out);
    } catch (err) {
      box.innerHTML = "<b>Error:</b> " + esc(err.message);
    } finally {
      btn.disabled = false;
    }
  });
}

bindSimple("qaForm", "question", "qaResult", "/qa", "question", "Answer:", "answer");
bindSimple("explainForm", "topic", "explainResult", "/explain", "topic", "Explanation:", "explanation");
bindSimple("summaryForm", "summaryText", "summaryResult", "/summarize", "text", "Summary:", "summary");
bindSimple("learnForm", "learnTopic", "learnResult", "/learn/recommendations", "topic", "Learning Path:", "recommendation");

var quizForm = el("quizForm");
if (quizForm) {
  quizForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    var value = el("quizText").value.trim();
    if (!value) return;

    var box = el("quizResult");
    var btn = quizForm.querySelector("button");
    btn.disabled = true;
    loading(box);

    try {
      var data = await postJSON("/quiz", { text: value });
      var quiz = data.quiz;

      box.innerHTML = "<b>Quiz:</b>";

      if (!Array.isArray(quiz) || quiz.length === 0 || quiz[0].error) {
        var msg = (quiz && quiz[0] && quiz[0].error) || "Could not generate quiz. Try again.";
        box.innerHTML += "\n\n" + esc(msg);
        return;
      }

      quiz.forEach(function (q, i) {
        var wrap = document.createElement("div");
        wrap.className = "quiz-q";

        var qt = document.createElement("span");
        qt.className = "qtext";
        qt.textContent = "Q" + (i + 1) + ": " + q.question;
        wrap.appendChild(qt);

        q.options.forEach(function (opt) {
          var lab = document.createElement("label");
          var radio = document.createElement("input");
          radio.type = "radio";
          radio.name = "quiz" + i;
          radio.value = opt;
          lab.appendChild(radio);
          lab.appendChild(document.createTextNode(" " + opt));
          wrap.appendChild(lab);
        });

        var check = document.createElement("button");
        check.type = "button";
        check.className = "check-btn";
        check.textContent = "Check Answer";

        var res = document.createElement("div");

        check.addEventListener("click", function () {
          var sel = wrap.querySelector('input[name="quiz' + i + '"]:checked');
          if (!sel) {
            res.className = "res warn";
            res.textContent = "Please select an option first.";
            return;
          }
          if (sel.value === q.answer) {
            res.className = "res ok";
            res.textContent = "Correct!";
          } else {
            res.className = "res no";
            res.textContent = "Incorrect. Correct answer: " + q.answer;
          }
        });

        wrap.appendChild(check);
        wrap.appendChild(res);
        box.appendChild(wrap);
      });
    } catch (err) {
      box.innerHTML = "<b>Error:</b> " + esc(err.message);
    } finally {
      btn.disabled = false;
    }
  });
}

console.log("EduGenie loaded");