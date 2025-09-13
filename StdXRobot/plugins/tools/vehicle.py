# plugins/vehicle.py
import httpx
from StdXRobot import app
from pyrogram import filters

API_URL = "https://vehicle-infoapi.vercel.app/api"
API_KEY = "test"

# helper: normalize dict keys
def normalize_dict(d: dict):
    return {k.lower().replace(" ", "_").replace("-", "_"): v for k, v in d.items()}

@app.on_message(filters.command("vehicle"))
async def vehicle_lookup(client, message):
    if len(message.command) < 2:
        await message.reply("❌ Usage: `/vehicle MH12AB1234`", quote=True)
        return

    reg_number = message.command[1].upper().replace("-", "").replace(" ", "")

    try:
        async with httpx.AsyncClient(timeout=30) as client_http:
            url = f"{API_URL}?vin={reg_number}&key={API_KEY}"
            response = await client_http.get(url)

        result = response.json()
        data = normalize_dict(result.get("processedData", {}))

        if not data:
            await message.reply("⚠️ No processed data found for this vehicle.", quote=True)
            return

        text = f"""
**🚦 Vehicle Info Report**
━━━━━━━━━━━━━━━
🔹 **Registration No:** `{data.get('meta_data_response_result_reg_no', 'N/A')}`
🔹 **Owner:** {data.get('meta_data_response_result_owner', 'N/A')}
🔹 **Owner Count:** {data.get('meta_data_response_result_owner_count', 'N/A')}
🔹 **Status:** {data.get('meta_data_response_result_status', 'N/A')} (as on {data.get('meta_data_response_result_status_as_on', 'N/A')})

**🛵 Vehicle Details**
🔸 Manufacturer: {data.get('meta_data_response_result_vehicle_manufacturer_name', 'N/A')}
🔸 Model: {data.get('meta_data_response_result_model', 'N/A')}
🔸 Colour: {data.get('meta_data_response_result_vehicle_colour', 'N/A')}
🔸 Type: {data.get('meta_data_response_result_type', 'N/A')}
🔸 Fuel: {data.get('meta_data_response_result_vehicle_category', 'N/A')}
🔸 CC: {data.get('meta_data_response_result_vehicle_cubic_capacity', 'N/A')}
🔸 Seats: {data.get('meta_data_response_result_vehicle_seat_capacity', 'N/A')}

**📅 Dates**
🔸 Reg Date: {data.get('meta_data_response_result_reg_date', 'N/A')}
🔸 Manufacture: {data.get('meta_data_response_result_vehicle_manufacturing_month_year', 'N/A')}
🔸 RC Expiry: {data.get('meta_data_response_result_rc_expiry_date', 'N/A')}
🔸 Insurance Upto: {data.get('meta_data_response_result_vehicle_insurance_upto', 'N/A')}

**🛡 Insurance**
🔸 Company: {data.get('meta_data_response_result_vehicle_insurance_company_name', 'N/A')}
🔸 Policy No: `{data.get('meta_data_response_result_vehicle_insurance_policy_number', 'N/A')}`

**🏢 RTO**
🔸 RTO Code: {data.get('rto_code', 'N/A')}
🔸 Authority: {data.get('meta_data_response_result_reg_authority', 'N/A')}

⚙️ **Source:** API by @STDXD
"""
        await message.reply(text, quote=True)

    except Exception as e:
        await message.reply(f"❌ Error: {e}", quote=True)
