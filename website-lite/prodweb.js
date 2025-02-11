
var text = "";
async function onLoad() {
    
    var name = document.getElementById("username").value;
    var key = document.getElementById("openaikey").value;
    console.log(name)
    console.log(key)

    try {

        data = {
            name: name,
            key: key
        }

        const response = await fetch("http://127.0.0.1:8000/onLoad/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch response from server");
        }

        const reply = await response.text();
        updateText(reply);
        sessionStorage.setItem("onLoadExecuted", "true");

    } catch (error) {
        console.error("Error fetching response:", error);
    }
}

function updateText(t) {
    text = t
    document.getElementById('hinaText').textContent=text;
}

function updateImage(res){
    const imageElement = document.getElementById('background_img');
    const imgUrl = "images/" + res + ".png"
    console.log("Updating image source to:", imgUrl);

    if (imageElement) {
        imageElement.src = imgUrl;
    } else {
        console.warn("⚠️ Image element not found!");
    }
}

async function submitForm(e) {
    e.preventDefault();

    var prompt = document.getElementById("reply").value;
    console.log(prompt)
    console.log(typeof(prompt))
    const data = {
        reply: prompt
    }

    try {
        const response = await fetch("http://127.0.0.1:8000/generate_response/", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`text Failed to fetch response from /generate_response/: ${response.status} ${response.statusText}`);
        }

        const reply = await response.text();
        console.log("reply: "+ reply)
        const res = clean_prompt_for_sd(reply)
        console.log("res:" + res)

        updateImage(res);
        updateText(reply);

    } catch (error) {
        console.error("Error fetching response:", error);
    }
}


function clean_prompt_for_sd(p) {
    const match = p.match(/\*(.*?)\*/);
    console.log("match: " + match)
    const extracted_prompt = match[1].trim();
    return extracted_prompt;
}

document.addEventListener("DOMContentLoaded", function () {
    console.log("DOM fully loaded");

    const toggleButton = document.getElementById("toggleButton");
    const textbox = document.getElementById("textbox");
    const buttonBackground = document.querySelector(".buttonbackground");
    const download = document.getElementById("downloadButton");

    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", submitForm);
    }

    const popupOverlay = document.getElementById("popupOverlay");
    const popupSubmit = document.getElementById("popupSubmit");

    popupOverlay.classList.add("active");

    popupSubmit.addEventListener("click", function (e) {
        e.preventDefault()
        onLoad()
        popupOverlay.classList.remove("active");
        console.log("popupOverlay hidden")
    });


    toggleButton.addEventListener("click", (event) => {
        event.stopPropagation();
        textbox.classList.add("hidden");
        toggleButton.style.display = "none";
        buttonBackground.style.display = "none";
        download.style.display = "none";

    });

    document.addEventListener("click", () => {
        textbox.classList.remove("hidden");
        toggleButton.style.display = "block";
        buttonBackground.style.display = "flex";
        download.style.display = "block";

    });

    textbox.addEventListener("click", (event) => {
        event.stopPropagation();
    });

});


// document.addEventListener("DOMContentLoaded", () => {
//     // if (!sessionStorage.getItem("onLoadExecuted")) {
//     //     onLoad(); 
//     // }
//     document.querySelector("form").addEventListener("submit", submitForm);
// });
