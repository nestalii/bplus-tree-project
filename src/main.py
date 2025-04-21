from bplustree import BPlusTree
from hash_function import hash_name

RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"

tree = BPlusTree(order=4)

with open("../data.txt", "r", encoding="utf-8") as file:
    for line in file:
        name = line.strip()
        if name:
            tree.insert(hash_name(name), name)

print("=" * 40)
print(f"{BOLD}{BLUE}Початкове дерево після вставки:{RESET}")
tree.print_tree()

delete_name = "Ілля"
tree.delete(hash_name(delete_name))
print(f"\n{BOLD}{RED}Видалення імені: {delete_name}{RESET}")
print("Поточна структура дерева:")
tree.print_tree()

post_delete = tree.search(hash_name(delete_name))
print(f"\n{BOLD}Перевірка пошуку після видалення: {delete_name}{RESET}")
print("Знайдено:" if post_delete else "Не знайдено:", post_delete)

target_name = "Дмитро"
result = tree.search(hash_name(target_name))
print(f"\n{BOLD}{GREEN}Пошук точного імені: {target_name}{RESET}")
print("Знайдено:" if result else "Не знайдено:", result)

compare_name = "Кос"
gt_results = tree.search_greater_than(hash_name(compare_name))
print(f"\n{BOLD}{YELLOW}Імена більші за: {compare_name}{RESET}")
for _, name in gt_results:
    print("-", name)

compare_name = "Л"
lt_results = tree.search_less_than(hash_name(compare_name))
print(f"\n{BOLD}{YELLOW}Імена менші за: {compare_name}{RESET}")
for _, name in lt_results:
    print("-", name)

print("=" * 40)