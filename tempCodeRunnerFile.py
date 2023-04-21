    with open('account_stats.json', 'w', encoding='utf-8') as f:
        json.dump(account_stats, f, ensure_ascii=False, indent=4)