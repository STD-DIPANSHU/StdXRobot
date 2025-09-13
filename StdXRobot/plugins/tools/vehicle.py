# StdXRobot/plugins/tools/vehicle.py

import httpx
from StdXRobot import app
from pyrogram import filters
from pyrogram.types import Message


API_URL = "https://vehicle-infoapi.vercel.app/"  # apna actual API endpoint daal


@app.on_message(filters.command(["vehicle", "rc"]))
async def vehicle_lookup(_, message: Message):
    if len(message.command) < 2:
        await message.reply("⚠️ Example: `/vehicle MH12AB1234`", quote=True)
        return

    reg_number = message.command[1]

    try:
        async with httpx.AsyncClient(timeout=30) as client_http:
            response = await client_http.get(f"{API_URL}?regno={reg_number}")
            if response.status_code != 200:
                await message.reply(f"❌ API Error: {response.status_code}", quote=True)
                return

            data = response.json().get("processedData", {})

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

━━━━━━━━━━━━━━━
⚡ Source: {data.get('source', 'API')}
"""
            await message.reply(text, quote=True, disable_web_page_preview=True)

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}", quote=True)
