from brain.reasoning import analyse_market

result = analyse_market(
    rsi=56,
    ema20=3380,
    ema50=3350,
    current_price=3395
)

print("=" * 50)
print("        IKA AI Analysis Report")
print("=" * 50)

print(f"Market Rating : {result['rating']}")
print(f"Confidence    : {result['score']}%")

print("\nReasons:")

for reason in result["reasons"]:
    print(f"✓ {reason}")
    
