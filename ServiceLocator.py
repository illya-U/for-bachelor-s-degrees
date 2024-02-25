class ServiceLocator:
    _services = {}

    @staticmethod
    def register_service(service_name, service):
        ServiceLocator._services[service_name] = service

    @staticmethod
    def get_service(service_name):
        service = ServiceLocator._services.get(service_name)
        if not service:
            raise ValueError(f"Service {service_name} not found")
        return service
