# vehicle.py
import httpx
from StdXRobot import app
from pyrogram import filters

API_URL = "https://vehicle-infoapi.vercel.app/api"
API_KEY = "test"  # apna API key

@app.on_message(filters.command("vehicle"))
async def vehicle_lookup(client, message):
    if len(message.command) < 2:
        await message.reply(
            "❌ Please provide a vehicle number.\n\nUsage: `/vehicle MH12AB1234`",
            quote=True
        )
        return

    reg_number = message.command[1].upper().replace("-", "").replace(" ", "")

    try:
        async with httpx.AsyncClient(timeout=30) as client_http:
            url = f"{API_URL}?vin={reg_number}&key={API_KEY}"
            response = await client_http.get(url)

        if response.status_code != 200:
            await message.reply(
                f"❌ API Error {response.status_code}\n\n{response.text[:400]}",
                quote=True
            )
            return

        try:
            data = response.json().get("processedData", {})
        except Exception:
            await message.reply(
                f"❌ Invalid JSON Response:\n\n{response.text[:400]}",
                quote=True
            )
            return

        if not data:
            await message.reply("⚠️ No processed data found for this vehicle.", quote=True)
            return

        # === FORMATTED REPORT ===
        text = f"""
**🚦 Vehicle Info Report**
━━━━━━━━━━━━━━━
🔹 **Registration No:** `{data.get('Meta Data Response Result Reg No', 'N/A')}`
🔹 **Owner:** {data.get('Meta Data Response Result Owner', 'N/A')}
🔹 **Owner Count:** {data.get('Meta Data Response Result Owner Count', 'N/A')}
🔹 **Status:** {data.get('Meta Data Response Result Status', 'N/A')} (as on {data.get('Meta Data Response Result Status As On', 'N/A')})

**🛵 Vehicle Details**
🔸 Manufacturer: {data.get('Meta Data Response Result Vehicle Manufacturer Name', 'N/A')}
🔸 Model: {data.get('Meta Data Response Result Model', 'N/A')}
🔸 Colour: {data.get('Meta Data Response Result Vehicle Colour', 'N/A')}
🔸 Type: {data.get('Meta Data Response Result Type', 'N/A')}
🔸 Fuel: {data.get('Meta Data Response Result Vehicle Type', 'N/A')}
🔸 CC: {data.get('Meta Data Response Result Vehicle Cubic Capacity', 'N/A')}
🔸 Seats: {data.get('Meta Data Response Result Vehicle Seat Capacity', 'N/A')}

**📅 Dates**
🔸 Reg Date: {data.get('Meta Data Response Result Reg Date', 'N/A')}
🔸 Manufacture: {data.get('Meta Data Response Result Vehicle Manufacturing Month Year', 'N/A')}
🔸 RC Expiry: {data.get('Meta Data Response Result Rc Expiry Date', 'N/A')}
🔸 Insurance Upto: {data.get('Meta Data Response Result Vehicle Insurance Upto', 'N/A')}

**🛡 Insurance**
🔸 Company: {data.get('Meta Data Response Result Vehicle Insurance Company Name', 'N/A')}
🔸 Policy No: `{data.get('Meta Data Response Result Vehicle Insurance Policy Number', 'N/A')}`

**🏢 RTO**
🔸 RTO Code: {data.get('Meta Data Response Result Rto Code', 'N/A')}
🔸 Authority: {data.get('Meta Data Response Result Reg Authority', 'N/A')}

⚙️ **Source:** API by @STDXD
"""
        await message.reply(text, quote=True)

    except Exception as e:
        await message.reply(f"❌ Error: {e}", quote=True)
