import argparse
import datetime as dt
import json
import os
import random

STATE_FILE = 'state.json'

CATEGORIES = {
    'pohyb': ['běh', 'cvičení', 'procházka'],
    'zdraví': ['vitamíny', 'zelenina k jídlu', 'strečink'],
    'volno': ['čtení', 'hudba', 'odpočinek'],
    'mindset': ['meditace', 'děkovný zápis', 'deník'],
    'ranni_rutina': ['sklenice vody', 'rozcvička', 'plánování dne'],
    'vecerni_rutina': ['reflexe', 'příprava věcí na ráno', 'čtení knihy'],
    'prace': ['projekt A', 'projekt B', 'úklid mailů'],
    'uceni': ['online kurz', 'studium knihy', 'procvičení']
}

PENALTIES = {
    'lehke': ['10 kliků', 'studená sprcha', '5 minut plank'],
    'stredni': ['běh 5 km', '30 minut úklid', 'omezení sociálních sítí'],
    'tezke': ['žádná televize celý den', '1 hodina intenzivního cvičení', 'den bez sladkostí']
}


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def generate_plan():
    state = load_state()
    today = str(dt.date.today())
    plans = state.setdefault('plans', {})
    if today in plans:
        return plans[today]

    yesterday = str(dt.date.today() - dt.timedelta(days=1))
    prev_plan = plans.get(yesterday, {}).get('tasks', {})

    tasks = {}
    for cat, options in CATEGORIES.items():
        available = [a for a in options if a != prev_plan.get(cat)] or options
        tasks[cat] = random.choice(available)

    penalties = {lvl: random.choice(lst) for lvl, lst in PENALTIES.items()}

    plan = {'tasks': tasks, 'penalties': penalties, 'done': {}}
    plans[today] = plan
    save_state(state)
    return plan


def show_plan(plan):
    print('--- Dnešní mise ---')
    for cat, task in plan['tasks'].items():
        status = '✅' if plan['done'].get(cat) else '❌'
        print(f'{cat}: {task} {status}')
    print('\nTresty:')
    for lvl, pen in plan['penalties'].items():
        print(f'{lvl}: {pen}')


def check_task(category):
    state = load_state()
    today = str(dt.date.today())
    plan = state.get('plans', {}).get(today)
    if not plan:
        print('Nejprve vygenerujte plán pomocí --generate.')
        return
    if category not in plan['tasks']:
        print('Neznámá kategorie.')
        return
    plan['done'][category] = True
    save_state(state)
    print(f'Úkol "{category}" označen jako splněný.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Disciplína HRAVĚ')
    parser.add_argument('--generate', action='store_true', help='Vygenerovat dnešní plán')
    parser.add_argument('--check', metavar='KATEGORIE', help='Označit úkol jako splněný')
    parser.add_argument('--show', action='store_true', help='Zobrazit dnešní plán')
    args = parser.parse_args()

    if args.generate:
        plan = generate_plan()
        show_plan(plan)
    elif args.check:
        check_task(args.check)
    else:
        state = load_state()
        plan = state.get('plans', {}).get(str(dt.date.today()))
        if plan:
            show_plan(plan)
        else:
            print('Dnešní plán ještě nebyl vytvořen. Spusťte s --generate.')
