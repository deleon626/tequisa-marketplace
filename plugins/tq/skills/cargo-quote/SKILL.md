---
name: cargo-quote
description: Generate cargo shipment quotes based on historical expedition data for Tequisa
disable-model-invocation: true
allowed-tools: Read
---

# Cargo Shipment Quote Generator

Generate accurate cargo shipment quotes based on Tequisa's historical expedition data. This skill analyzes product type, weight, destination, and urgency to recommend the best expedition options with detailed cost breakdowns.

## How to Use

Invoke this skill with a natural language description containing:
- **Product type**: "liquid", "general cargo", "cairan", etc.
- **Weight**: "100kg", "50 kilos", "25 liter", etc.
- **Destination**: City or region name
- **Urgency** (optional): "express", "urgent", "regular"

**Example**:
```
/cargo-quote 100kg general cargo to Surabaya
/cargo-quote 25 liter liquid product to Bandung urgent
/cargo-quote 150kg to Medan express
```

## Processing Instructions

When this skill is invoked with `$ARGUMENTS`:

### Step 1: Read Historical Data
Load `/Users/dennyleonardo/Downloads/cargo-shipment-data.md` and parse the expedition data table.

### Step 2: Parse Input Description ($ARGUMENTS)
Extract the following information from the user's description:

1. **Weight (kg)**:
   - Look for patterns: "100kg", "100 kg", "100 kilos", "100 kilogram"
   - Also accept "liter" or "L" (assume 1L ≈ 1kg for estimation)
   - Examples: "100kg" → 100, "50 kilos" → 50, "25 liter" → 25

2. **Destination**:
   - Match against known destinations in the data (case-insensitive, partial match OK)
   - Common destinations: Surabaya, Medan, Bali, Jawa Barat, Jawa Tengah, Jawa Timur, Bandung, etc.
   - Handle regional groupings (e.g., "Jawa Timur 1" includes specific cities)

3. **Product Type**:
   - Detect if "liquid", "cairan", "cair" → flag as liquid cargo
   - Otherwise, treat as general cargo

4. **Urgency**:
   - Keywords: "express", "urgent", "fast", "cepat" → prioritize express services
   - Keywords: "regular", "reguler", "ekonomis" → prioritize regular services
   - If not specified, show both

### Step 3: Match Expeditions

Filter expeditions from the historical data based on:

1. **Destination Match**:
   - Exact match preferred
   - Partial match acceptable (e.g., "Surabaya" matches any service to Surabaya)
   - Regional match (e.g., if destination is in "Jawa Barat", match services to that region)

2. **Service Type**:
   - If urgency = express: prioritize "Express" services
   - If urgency = regular: prioritize "Reguler" services
   - Show all options if no preference

3. **Minimum Quantity Requirements**:
   - Check if weight meets minimum qty
   - If below minimum, note it in output but still show the option
   - Many expeditions require 100kg minimum

4. **Product Type Restrictions**:
   - Liquid cargo → exclude air cargo (Alam Sejahtera Logistik notes "CAIRAN TIDAK BISA")
   - Liquid cargo → flag wooden packing requirement for Panca Kobra Sakti

### Step 4: Calculate Estimated Costs

For each matching expedition, calculate total cost based on the pricing structure:

#### Pricing Patterns:

1. **Per kg rate** (e.g., "850/kg"):
   ```
   Base cost = weight × rate_per_kg
   ```

2. **Tiered rate** (e.g., "50000 for 5kg, then 1100/kg"):
   ```
   If weight ≤ 5kg: Base cost = 50000
   If weight > 5kg: Base cost = 50000 + (weight - 5) × 1100
   ```

3. **Volume rate** (e.g., "1,270,000/M.3"):
   - Note that this requires volume calculation
   - Show as "Volume-based pricing - contact for exact quote"

#### Additional Fees:

1. **Penerus Fees** (forwarding fees to specific destinations):
   - Situbondo: +45,000/coly
   - Tuban: +900,000
   - Gresik: +350,000
   - Add to base cost if destination requires penerus

2. **Packing Fees**:
   - Liquid cargo via Panca Kobra Sakti: +100,000/coly (for wooden packing)
   - Note: 1 coly can fit 2 drums @ 25L each
   - Calculate number of coly needed based on volume

3. **Admin Fees**:
   - Alam Sejahtera Logistik (air cargo): +15,000 admin fee
   - Add to base cost

4. **Per Coly Fees**:
   - Some services charge per coly (e.g., "15,000/Coly")
   - Estimate coly count from weight (typically 1 coly ≈ 50-100kg)

#### Cost Range:
- If exact calculation possible: show single amount
- If uncertainty exists: show range (min-max)
- Always show breakdown: "Base (X) + Fees (Y) = Total (Z)"

### Step 5: Sort and Format Output

Sort results by **estimated total cost** (lowest to highest).

Use this output format:

```
📦 CARGO QUOTE RESULTS
Request: [summarize parsed input - e.g., "100kg general cargo to Surabaya"]

Found [N] matching expedition(s):

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣ [Expedition Name] - [Service Type]
   💰 Estimated Cost: Rp [amount] (Base: [X] + Fees: [Y])
   ⏱️  ETA: [delivery time]
   📞 Contact: [PIC name] - [phone number]
   📦 Min Qty: [minimum quantity if applicable]
   ⚠️  Notes: [special requirements/warnings]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

2️⃣ [Next expedition...]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 IMPORTANT NOTES:
[Include relevant notes based on product type and destination]
- Liquid cargo requires wooden packing (+100,000/coly, 1 coly = 2 drums @ 25L)
- Bali via Gemilang: Pickup at Pertigaan Cekik (cannot deliver to address)
- Air cargo: Port-to-port service, pickup required at destination airport
- Penerus fees apply for certain destinations (additional forwarding cost)

📊 SUMMARY:
- Price range: Rp [lowest] - Rp [highest]
- Fastest option: [expedition name] ([ETA])
- Cheapest option: [expedition name] (Rp [amount])
```

## Special Handling Rules

### Liquid Cargo
When product type is "liquid" or "cairan":
1. **Exclude air cargo** (Alam Sejahtera Logistik)
2. **Flag wooden packing requirement**:
   - Panca Kobra Sakti: "BARANG CAIRAN WAJIB PAKING KAYU"
   - Cost: +100,000/coly
   - 1 coly can pack 2 drums @ 25L each
3. **Calculate coly needed**:
   - If weight/volume provided, estimate: coly_count = ceil(liters / 50)
   - Add packing cost: packing_fee = coly_count × 100,000

### Destination-Specific Notes
1. **Bali (via Gemilang)**:
   - Note: "Tidak bisa antar alamat tujuan, pengambilan di Pertigaan Cekik"
   - Translation: Cannot deliver to address, pickup at Pertigaan Cekik

2. **Situbondo (via Mojoroto Express)**:
   - Base rate + penerus fee
   - Example calculation shown in data: "100kg × 850 = 85,000 + 45,000 (1 coly) = 130,000"

3. **Tuban, Gresik (via Mojoroto Express)**:
   - Significant penerus fees (900,000 for Tuban, 350,000 for Gresik)

4. **Jawa Timur Regions**:
   - Jawa Timur 1: Cepu, Blora, Sragen, Wonogiri, Tulungagung
   - Jawa Timur 2: Situbondo, Bondowoso

### Air Cargo (Alam Sejahtera Logistik)
1. **Port-to-port only**
2. **No liquid cargo** ("CAIRAN TIDAK BISA")
3. **Additional charges at destination**:
   - "ADA BIAYA TAMBAHAN PADA SAAT PENGAMBILAN BARANG DI GUDANG TUJUAN"
   - Note: Costs determined by destination warehouse
4. **Admin fee**: +15,000
5. **Transit required** for outer islands ("UNTUK LUAR PULAU ADA TRANSIT")

### Minimum Quantity Warnings
If weight < minimum qty for an expedition:
- Still show the option
- Add warning: "⚠️ Below minimum quantity (min: [X]kg) - may not be available"

### Missing Data Handling
Many fields contain "nan" in the data:
- If price is "nan": Show "Contact for quote"
- If ETA is "nan": Show "Contact for ETA"
- If phone/PIC is "nan": Show "Contact via main office"

## Example Calculations

### Example 1: Simple Per-Kg Rate
**Input**: "100kg to Surabaya regular"
**Expedition**: Mojoroto Express - Reguler
- Base rate: 850/kg
- Weight: 100kg
- Calculation: 100 × 850 = 85,000
- **Total: Rp 85,000**

### Example 2: Tiered Rate
**Input**: "50kg to Bandung"
**Expedition**: Panca Kobra Sakti - Jawa Barat
- First 5kg: 50,000
- Additional: (50-5) × 1,100 = 49,500
- **Total: Rp 99,500**

### Example 3: With Penerus Fee
**Input**: "100kg to Situbondo"
**Expedition**: Mojoroto Express
- Base: 100 × 850 = 85,000
- Penerus fee: 45,000/coly
- Assume 1 coly for 100kg
- **Total: Rp 130,000** (matches example in data)

### Example 4: Liquid with Packing
**Input**: "50 liter liquid to Bandung"
**Expedition**: Panca Kobra Sakti - Jawa Barat
- Weight equivalent: ~50kg
- First 5kg: 50,000
- Additional: (50-5) × 1,100 = 49,500
- Wooden packing: 100,000/coly (need 1 coly for 50L)
- **Total: Rp 199,500** (Base: 99,500 + Packing: 100,000)

### Example 5: Air Cargo
**Input**: "10kg urgent to Medan"
**Expedition**: Alam Sejahtera Logistik
- Base: 33,000 (for 10kg to Medan)
- Admin: 15,000
- **Total: Rp 48,000**
- Note: Port-to-port, additional pickup fees at destination

## Data Source Reference

All pricing and expedition information is sourced from:
`/Users/dennyleonardo/Downloads/cargo-shipment-data.md`

This file contains historical shipment data including:
- Expedition names and contacts
- Pricing structures
- Service areas and destinations
- ETAs and special requirements
- Notes and examples from past shipments
