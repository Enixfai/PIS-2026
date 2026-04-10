# Архитектура Ticket Service (HelpDesk)

Сервис спроектирован на основе паттерна **Hexagonal Architecture (Ports and Adapters)**. 
Главная цель — полная изоляция доменной бизнес-логики (Ядра) от деталей инфраструктуры (БД, брокеры сообщений, веб-фреймворки).

## Архитектурная C4 Диаграмма (Контейнеры и Компоненты)

```plantuml
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

LAYOUT_WITH_LEGEND()

title Компонентная диаграмма (Гексагональная архитектура) - Ticket Service

Container_Boundary(api, "Ticket Service Application") {
    
    Component_Boundary(infra, "Infrastructure Layer") {
        Component(rest_api, "REST Controller", "FastAPI", "Принимает HTTP запросы (Inbound Adapter)")
        Component(db_adapter, "PostgreSQL Adapter", "SQLAlchemy", "Работа с БД (Outbound Adapter)")
        Component(rabbit_adapter, "RabbitMQ Adapter", "Pika", "Отправка событий (Outbound Adapter)")
    }

    Component_Boundary(app, "Application Layer") {
        Component(in_port, "CreateTicketUseCase", "Interface (Inbound Port)", "Интерфейс для клиентских запросов")
        Component(app_service, "TicketService", "Python Class", "Оркестрация use-case'ов")
        Component(out_repo, "TicketRepository", "Interface (Outbound Port)", "Контракт для хранилища")
        Component(out_broker, "NotificationPort", "Interface (Outbound Port)", "Контракт для брокера")
    }

    Component_Boundary(domain, "Domain Layer") {
        Component(ticket, "Ticket", "Entity", "Чистая бизнес-логика и правила")
    }
}

Rel(rest_api, in_port, "Использует", "Методы интерфейса")
Rel(in_port, app_service, "Реализуется классом")
Rel(app_service, ticket, "Управляет сущностями")

Rel(app_service, out_repo, "Вызывает интерфейс")
Rel(app_service, out_broker, "Вызывает интерфейс")

Rel(db_adapter, out_repo, "Имплементирует")
Rel(rabbit_adapter, out_broker, "Имплементирует")

@enduml