let interval = null;

function startSim() {
    fetch('/start');

    interval = setInterval(() => {
        runStep();
    }, 2000); // every 2 sec
}

function runStep() {
    fetch('/step')
        .then(res => res.json())
        .then(data => {
            if (!data) return;

            let div = document.getElementById("timeline");

            let block = document.createElement("div");
            block.innerHTML = `
              <b>${data.time}</b><br>
              <i>Event: ${data.event}</i><br><br>
              ${data.logs.join("<br>")}`;

            div.appendChild(block);
        });
}

function stopSim() {
    fetch('/stop');
    clearInterval(interval);
}