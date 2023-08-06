import json
import signal as os_signal
import os
from time import sleep
from typing import List
from rich import print as rich_rprint

import typer
from zeroconf import (
    IPVersion,
    ServiceBrowser,
    ServiceStateChange,
    Zeroconf,
)

from .lib.broker import Broker

app = typer.Typer()


@app.command(help="List signals on broker")
def signals(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token", envvar='REMOTIVE_BROKER_API_KEY')
):
    broker = Broker(url, api_key)
    # print("Listing available signals")
    available_signals = broker.list_signal_names()
    print(json.dumps(available_signals))


@app.command(help="List signals on broker")
def subscribe(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token", envvar='REMOTIVE_BROKER_API_KEY'),
        signal: List[str] = typer.Option(..., help="Roles to apply"),
        namespace: str = typer.Option(..., help="Cloud Broker API-KEY or access token", envvar='REMOTIVE_BROKER_API_KEY'),
        on_change_only: bool = typer.Option(default=False, help="Only get signal if value is changed"),
        #samples: int = typer.Option(default=0, he)

):
    broker = Broker(url, api_key)
    print("Subscribing to signals, press Ctrl+C to exit")

    def exit_on_ctrlc(sig, frame):
        os._exit(0)

    def on_frame_func(x):
        rich_rprint(json.dumps(list(x)))

    os_signal.signal(os_signal.SIGINT, exit_on_ctrlc)
    broker.subscribe(signal, namespace, on_frame_func, on_change_only)


@app.command(help="List namespaces on broker")
def namespaces(
        url: str = typer.Option(..., help="Broker URL", envvar='REMOTIVE_BROKER_URL'),
        api_key: str = typer.Option("offline", help="Cloud Broker API-KEY or access token", envvar='REMOTIVE_BROKER_API_KEY')
):
    broker = Broker(url, api_key)
    namespaces_json = broker.list_namespaces()
    print(json.dumps(namespaces_json))


@app.command(help="Discover brokers on this network")
def discover():
    # print("Not implemented")

    zeroconf = Zeroconf(ip_version=IPVersion.V4Only)

    services = ["_remotivebroker._tcp.local.", "_googlecast._tcp.local."]
    # services = list(ZeroconfServiceTypes.find(zc=zeroconf))

    print("\nLooking for RemotiveBrokers on your network, press Ctrl-C to exit...\n")
    browser = ServiceBrowser(zeroconf, services, handlers=[on_service_state_change])

    try:
        while True:
            sleep(0.1)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf.close()


def on_service_state_change(
        zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange
) -> None:
    # print(f"Service {name} state changed: {state_change}")

    if state_change is ServiceStateChange.Removed:
        print(f"Service {name} was removed")

    if state_change is ServiceStateChange.Updated:
        print(f"Service {name} was updated")

    if state_change is ServiceStateChange.Added:
        print(f"Discovered {name} ")
        info = zeroconf.get_service_info(service_type, name)
        # print("Info from zeroconf.get_service_info: %r" % (info))

        if info:
            # addresses = ["%s:%d" % (addr, cast(int, info.port)) for addr in info.parsed_scoped_addresses()]
            for addr in info.parsed_scoped_addresses():
                print(addr)
            # print("  Weight: %d, priority: %d" % (info.weight, info.priority))
            # print(f"  Server: {info.server}")
            # if info.properties:
            #    print("  Properties are:")
            #    for key, value in info.properties.items():
            #        print(f"    {key}: {value}")
            # else:
            #    print("  No properties")
        else:
            print("  No info")
        print('\n')


if __name__ == "__main__":
    app()
