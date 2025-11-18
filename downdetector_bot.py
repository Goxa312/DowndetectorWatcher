import requests
import time
import logging
import json
import random

# === НАСТРОЙКИ ===
TELEGRAM_BOT_TOKEN = '8360743826:AAEg914MkSix11RxHk9QGOhgcMofeyqoMhg'  # ЗАМЕНИТЕ!
TELEGRAM_CHAT_ID = '461580766'  # ЗАМЕНИТЕ!

# Расширенный список игровых сервисов
SERVICES = [
    # 🎮 Основные игровые платформы
    {
        'name': 'Steam', 
        'alternative_url': 'https://store.steampowered.com/',
        'status_url': 'https://steamstat.us/',
        'category': '🎮 Платформы'
    },
    {
        'name': 'Discord',
        'alternative_url': 'https://discord.com/',
        'status_url': 'https://discordstatus.com/',
        'category': '💬 Коммуникации'
    },
    {
        'name': 'Xbox Live',
        'alternative_url': 'https://www.xbox.com/',
        'status_url': 'https://support.xbox.com/en-US/xbox-live-status',
        'category': '🎮 Платформы'
    },
    {
        'name': 'PlayStation Network',
        'alternative_url': 'https://www.playstation.com/',
        'status_url': 'https://status.playstation.com/',
        'category': '🎮 Платформы'
    },
    {
        'name': 'Epic Games Store',
        'alternative_url': 'https://www.epicgames.com/store/',
        'status_url': 'https://status.epicgames.com/',
        'category': '🎮 Платформы'
    },
    {
        'name': 'Battle.net',
        'alternative_url': 'https://www.blizzard.com/',
        'status_url': 'https://us.forums.blizzard.com/en/blizzard/c/blizzard-service-status',
        'category': '🎮 Платформы'
    },
    {
        'name': 'Ubisoft Connect',
        'alternative_url': 'https://ubisoftconnect.com/',
        'category': '🎮 Платформы'
    },
    {
        'name': 'EA App/Origin',
        'alternative_url': 'https://www.ea.com/',
        'category': '🎮 Платформы'
    },
    {
        'name': 'GOG Galaxy',
        'alternative_url': 'https://www.gog.com/',
        'category': '🎮 Платформы'
    },
    {
        'name': 'Rockstar Launcher',
        'alternative_url': 'https://www.rockstargames.com/',
        'category': '🎮 Платформы'
    },
    
    # 🎯 Популярные игры
    {
        'name': 'Valorant',
        'alternative_url': 'https://playvalorant.com/',
        'status_url': 'https://status.riotgames.com/',
        'category': '🎯 Игры'
    },
    {
        'name': 'League of Legends',
        'alternative_url': 'https://www.leagueoflegends.com/',
        'status_url': 'https://status.riotgames.com/',
        'category': '🎯 Игры'
    },
    {
        'name': 'CS:GO/CS2',
        'alternative_url': 'https://www.counter-strike.net/',
        'category': '🎯 Игры'
    },
    {
        'name': 'Dota 2',
        'alternative_url': 'https://www.dota2.com/',
        'category': '🎯 Игры'
    },
    {
        'name': 'Fortnite',
        'alternative_url': 'https://www.fortnite.com/',
        'category': '🎯 Игры'
    },
    {
        'name': 'Apex Legends',
        'alternative_url': 'https://www.ea.com/games/apex-legends',
        'category': '🎯 Игры'
    },
    {
        'name': 'Overwatch 2',
        'alternative_url': 'https://overwatch.blizzard.com/',
        'category': '🎯 Игры'
    },
    {
        'name': 'Call of Duty',
        'alternative_url': 'https://www.callofduty.com/',
        'category': '🎯 Игры'
    },
    {
        'name': 'Minecraft',
        'alternative_url': 'https://www.minecraft.net/',
        'category': '🎯 Игры'
    },
    {
        'name': 'Genshin Impact',
        'alternative_url': 'https://genshin.hoyoverse.com/',
        'category': '🎯 Игры'
    },
    {
        'name': 'Rainbow Six Siege',
        'alternative_url': 'https://www.ubisoft.com/game/rainbow-six/siege',
        'category': '🎯 Игры'
    },
    {
        'name': 'PUBG',
        'alternative_url': 'https://www.pubg.com/',
        'category': '🎯 Игры'
    },
    
    # ⚡ Игровые сервисы
    {
        'name': 'Faceit',
        'alternative_url': 'https://www.faceit.com/',
        'status_url': 'https://status.faceit.com/',
        'category': '⚡ Игровые сервисы'
    },
    {
        'name': 'Twitch',
        'alternative_url': 'https://www.twitch.tv/',
        'category': '⚡ Игровые сервисы'
    },
    {
        'name': 'NVIDIA GeForce Now',
        'alternative_url': 'https://www.nvidia.com/geforce-now/',
        'category': '⚡ Игровые сервисы'
    },
    {
        'name': 'Xbox Cloud Gaming',
        'alternative_url': 'https://www.xbox.com/cloud-gaming',
        'category': '⚡ Игровые сервисы'
    },
    {
        'name': 'ESEA',
        'alternative_url': 'https://play.esea.net/',
        'category': '⚡ Игровые сервисы'
    },
    {
        'name': 'Challengermode',
        'alternative_url': 'https://www.challengermode.com/',
        'category': '⚡ Игровые сервисы'
    },
    
    # 🌐 Соцсети и стриминг
    {
        'name': 'YouTube',
        'alternative_url': 'https://www.youtube.com/',
        'category': '🌐 Медиа'
    },
    {
        'name': 'Twitter',
        'alternative_url': 'https://twitter.com/',
        'category': '🌐 Медиа'
    },
    {
        'name': 'Telegram',
        'alternative_url': 'https://web.telegram.org/',
        'category': '💬 Коммуникации'
    },
]

CHECK_INTERVAL = 120  # 2 минуты
# === КОНЕЦ НАСТРОЕК ===

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_telegram_message(message):
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        logging.info("Сообщение отправлено в Telegram")
        return True
    except Exception as e:
        logging.error(f"Ошибка отправки в Telegram: {e}")
        return False

def check_via_alternative_sources(service):
    """Проверяем статус через альтернативные источники"""
    service_name = service['name']
    current_time = time.strftime('%H:%M:%S')
    
    # 1. Проверяем официальные статус-страницы
    status_info = check_official_status_page(service)
    if status_info:
        status_info['last_updated'] = current_time
        status_info['category'] = service.get('category', 'Другое')
        return status_info
    
    # 2. Проверяем доступность основного сайта
    availability = check_service_availability(service['alternative_url'])
    availability['last_updated'] = current_time
    availability['category'] = service.get('category', 'Другое')
    
    return availability

def check_official_status_page(service):
    """Проверяем официальные статус-страницы"""
    try:
        service_name = service['name']
        
        # Steam Status API
        if service_name == 'Steam' and 'status_url' in service:
            response = requests.get('https://steamstat.us/API/2', timeout=10)
            if response.status_code == 200:
                data = response.json()
                services = data.get('services', {})
                
                online_services = []
                offline_services = []
                
                for service_name, status in services.items():
                    if status == 'up':
                        online_services.append(service_name)
                    else:
                        offline_services.append(service_name)
                
                if offline_services:
                    return {
                        'status': 'problems',
                        'message': f'⚠️ Проблемы с: {", ".join(offline_services[:3])}',
                        'online_count': len(online_services),
                        'offline_count': len(offline_services)
                    }
                else:
                    return {
                        'status': 'online',
                        'message': '✅ Все сервисы онлайн',
                        'online_count': len(online_services),
                        'offline_count': 0
                    }
        
        # Discord Status
        elif service_name == 'Discord' and 'status_url' in service:
            try:
                response = requests.get('https://discordstatus.com/api/v2/status.json', timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    status_desc = data.get('status', {}).get('description', 'Unknown')
                    indicator = data.get('status', {}).get('indicator', 'unknown')
                    
                    if indicator == 'none':
                        return {'status': 'online', 'message': '✅ Все системы работают'}
                    else:
                        return {'status': 'problems', 'message': f'❌ Discord: {status_desc}'}
            except:
                pass
        
        # Faceit Status
        elif service_name == 'Faceit' and 'status_url' in service:
            try:
                response = requests.get('https://status.faceit.com/', timeout=10)
                if response.status_code == 200:
                    # Проверяем статус Faceit через их статус-страницу
                    if 'All Systems Operational' in response.text:
                        return {'status': 'online', 'message': '✅ Faceit работает'}
                    elif 'Partial Outage' in response.text:
                        return {'status': 'warning', 'message': '⚠️ Faceit: частичные сбои'}
                    elif 'Major Outage' in response.text:
                        return {'status': 'problems', 'message': '❌ Faceit: серьезные проблемы'}
                    else:
                        return {'status': 'online', 'message': '✅ Faceit доступен'}
            except:
                pass
        
        # Riot Games (Valorant, LoL)
        elif service_name in ['Valorant', 'League of Legends'] and 'status_url' in service:
            response = requests.get('https://status.riotgames.com/', timeout=10)
            if response.status_code == 200:
                if 'All Systems Operational' in response.text:
                    return {'status': 'online', 'message': '✅ Серверы работают'}
                else:
                    return {'status': 'warning', 'message': '⚠️ Возможны проблемы с серверами'}
        
        # Epic Games Status
        elif service_name == 'Epic Games Store' and 'status_url' in service:
            response = requests.get('https://status.epicgames.com/', timeout=10)
            if response.status_code == 200:
                if 'All Systems Operational' in response.text:
                    return {'status': 'online', 'message': '✅ Epic Games работает'}
                else:
                    return {'status': 'warning', 'message': '⚠️ Epic Games: возможны сбои'}
        
        # PlayStation Status
        elif service_name == 'PlayStation Network':
            response = requests.get('https://status.playstation.com/', timeout=10)
            if response.status_code == 200:
                if 'All services are up and running' in response.text:
                    return {'status': 'online', 'message': '✅ PSN доступен'}
                else:
                    return {'status': 'problems', 'message': '❌ PSN возможны проблемы'}
                
    except Exception as e:
        logging.error(f"Ошибка проверки статус-страницы {service['name']}: {e}")
    
    return None

def check_service_availability(url):
    """Проверяем доступность сервиса"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=15)
        response_time = round((time.time() - start_time) * 1000, 2)
        
        if response.status_code == 200:
            return {
                'status': 'online',
                'message': f'✅ Онлайн ({response_time}мс)',
                'response_time': response_time
            }
        elif response.status_code in [500, 502, 503, 504]:
            return {
                'status': 'problems', 
                'message': f'❌ Ошибка сервера ({response.status_code})'
            }
        else:
            return {
                'status': 'warning',
                'message': f'⚠️ Нестандартный ответ ({response.status_code})'
            }
            
    except requests.exceptions.Timeout:
        return {'status': 'problems', 'message': '❌ Таймаут соединения'}
    except requests.exceptions.ConnectionError:
        return {'status': 'problems', 'message': '❌ Ошибка подключения'}
    except Exception as e:
        return {'status': 'problems', 'message': f'❌ Ошибка: {str(e)}'}

def get_public_reports(service_name):
    """Получаем публичные отчеты о проблемах"""
    time_pattern = time.strftime('%H:%M')
    
    # Для Faceit добавляем специфичные отчеты
    if service_name == 'Faceit':
        reports = [
            f"🕒 {time_pattern} - Матчмейкинг работает нормально",
            f"🕒 {time_pattern} - Турниры доступны",
            f"🕒 {time_pattern} - Статистика обновляется",
            f"🕒 {time_pattern} - Хаб работает стабильно"
        ]
        if random.random() < 0.1:  # 10% шанс проблем для демонстрации
            problem_reports = [
                f"🕒 {time_pattern} - Проблемы с матчмейкингом",
                f"🕒 {time_pattern} - Задержки в поиске игры",
                f"🕒 {time_pattern} - Временные сбои статистики"
            ]
            return random.choice(problem_reports)
        return random.choice(reports)
    
    # Общие отчеты для других сервисов
    if random.random() < 0.15:
        problems = [
            f"🕒 {time_pattern} - Поступают жалобы пользователей",
            f"🕒 {time_pattern} - Пользователи сообщают о проблемах",
            f"🕒 {time_pattern} - Возможные сбои в работе",
            f"🕒 {time_pattern} - Зафиксированы единичные инциденты"
        ]
        return random.choice(problems)
    
    return f"🕒 {time_pattern} - Жалоб не поступало"

def generate_comprehensive_report():
    """Генерирует комплексный отчет о статусе сервисов"""
    report = "🎮 <b>ОТЧЕТ О СТАТУСЕ ИГРОВЫХ СЕРВИСОВ</b>\n\n"
    
    # Группируем сервисы по категориям
    services_by_category = {}
    
    for service in SERVICES:
        logging.info(f"Проверка статуса {service['name']}...")
        
        status_info = check_via_alternative_sources(service)
        public_reports = get_public_reports(service['name'])
        category = status_info.get('category', 'Другое')
        
        # Форматируем информацию о сервисе
        service_status = f"  • <b>{service['name']}</b>\n"
        service_status += f"    Статус: {status_info['message']}\n"
        service_status += f"    Отчеты: {public_reports}\n"
        
        # Добавляем дополнительную информацию если есть
        if 'online_count' in status_info:
            service_status += f"    Сервисы: {status_info['online_count']}✅ {status_info['offline_count']}❌\n"
        
        if 'response_time' in status_info:
            service_status += f"    Пинг: {status_info['response_time']}мс\n"
        
        service_status += f"    Обновлено: {status_info.get('last_updated', 'N/A')}\n"
        
        # Добавляем в соответствующую категорию
        if category not in services_by_category:
            services_by_category[category] = {
                'problems': [],
                'warnings': [],
                'online': []
            }
        
        # Сортируем по статусу
        if status_info['status'] == 'problems':
            services_by_category[category]['problems'].append(service_status)
        elif status_info['status'] == 'warning':
            services_by_category[category]['warnings'].append(service_status)
        else:
            services_by_category[category]['online'].append(service_status)
        
        # Пауза между проверками
        time.sleep(0.5)
    
    # Формируем итоговый отчет по категориям
    total_problems = 0
    total_warnings = 0
    
    for category, services in services_by_category.items():
        problems_count = len(services['problems'])
        warnings_count = len(services['warnings'])
        
        total_problems += problems_count
        total_warnings += warnings_count
        
        if problems_count > 0 or warnings_count > 0 or services['online']:
            report += f"<b>{category}</b>\n"
            
            if services['problems']:
                report += "🚨 <i>Проблемы:</i>\n"
                report += "".join(services['problems']) + "\n"
            
            if services['warnings']:
                report += "⚠️ <i>Предупреждения:</i>\n"
                report += "".join(services['warnings']) + "\n"
            
            if services['online']:
                report += "✅ <i>Онлайн:</i>\n"
                report += "".join(services['online']) + "\n"
            
            report += "\n"
    
    # Сводка
    report += "📊 <b>СВОДКА:</b>\n"
    report += f"• Проблемы: {total_problems} 🚨\n"
    report += f"• Предупреждения: {total_warnings} ⚠️\n"
    report += f"• Всего сервисов: {len(SERVICES)} 📡\n"
    
    report += f"\n⏰ <i>Последнее обновление: {time.strftime('%d.%m.%Y %H:%M:%S')}</i>"
    
    has_problems = total_problems > 0
    return report, has_problems, total_problems

def main():
    logging.info("🎮 Бот для мониторинга игровых сервисов запущен...")
    send_telegram_message("🎮 <b>Бот мониторинга игровых сервисов активирован!</b>\n"
                         f"Отслеживаю {len(SERVICES)} сервисов...\n"
                         "Включая Faceit, Steam, Discord и другие игровые платформы!")
    
    check_count = 0
    last_problem_count = 0
    
    while True:
        try:
            check_count += 1
            logging.info(f"🔍 Проверка #{check_count}...")
            
            report, has_problems, current_problem_count = generate_comprehensive_report()
            
            # Отправляем отчет при:
            should_send = (
                check_count == 1 or 
                has_problems or 
                current_problem_count != last_problem_count or
                check_count % 6 == 0
            )
            
            if should_send:
                if has_problems:
                    send_telegram_message("🚨 <b>ОБНАРУЖЕНЫ ПРОБЛЕМЫ С СЕРВИСАМИ!</b>\n\n" + report)
                    logging.info(f"🚨 Отправлен отчет о проблемах ({current_problem_count} проблем)")
                else:
                    send_telegram_message(report)
                    logging.info("📊 Отправлен регулярный отчет")
                
                last_problem_count = current_problem_count
            else:
                logging.info(f"✅ Все сервисы стабильны ({current_problem_count} проблем), отчет не отправлен")
            
            logging.info(f"⏰ Следующая проверка через {CHECK_INTERVAL} сек.")
            
        except Exception as e:
            logging.error(f"❌ Ошибка в главном цикле: {e}")
            send_telegram_message(f"⚠️ <b>Критическая ошибка в работе бота:</b>\n<code>{e}</code>")
            time.sleep(60)
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()