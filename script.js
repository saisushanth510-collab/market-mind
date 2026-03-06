// Campaign Generator
async function generateCampaign() {

    const product = document.getElementById("product").value;
    const audience = document.getElementById("audience").value;
    const platform = document.getElementById("platform").value;

    const response = await fetch("/generate_campaign", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product: product,
            audience: audience,
            platform: platform
        })
    });

    const data = await response.json();

    document.getElementById("campaignResult").innerText = data.campaign;
}



// Sales Pitch Generator
async function generatePitch() {

    const product = document.getElementById("pitchProduct").value;
    const customer = document.getElementById("customer").value;

    const response = await fetch("/generate_pitch", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            product: product,
            customer: customer
        })
    });

    const data = await response.json();

    document.getElementById("pitchResult").innerText = data.pitch;
}



// Lead Score Generator
async function scoreLead() {

    const name = document.getElementById("name").value;
    const budget = document.getElementById("budget").value;
    const need = document.getElementById("need").value;
    const urgency = document.getElementById("urgency").value;

    const response = await fetch("/lead_score", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            budget: budget,
            need: need,
            urgency: urgency
        })
    });

    const data = await response.json();

    document.getElementById("leadResult").innerText = data.score;
}