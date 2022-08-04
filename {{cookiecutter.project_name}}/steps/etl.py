from steps.user.scraper import BoligScrapper, BoligMarket

base_urls = {
    "Vesterbro": "https://www.boligsiden.dk/postnummer/1500/solgte/ejerlejlighed?sortAscending=true",
    "Copenhagen": "https://www.boligsiden.dk/postnummer/1000/solgte/ejerlejlighed?sortAscending=true",
    "Frederiskberg": "https://www.boligsiden.dk/postnummer/1800/solgte/ejerlejlighed?sortAscending=true",
    "Osterbro": "https://www.boligsiden.dk/postnummer/2100/solgte/ejerlejlighed?sortAscending=true",
    "Norrebro": "https://www.boligsiden.dk/postnummer/2200/solgte/ejerlejlighed?sortAscending=true",
    "Sydhavn": "https://www.boligsiden.dk/postnummer/2300/solgte/ejerlejlighed?sortAscending=true",
    "Nordvest": "https://www.boligsiden.dk/postnummer/2400/solgte/ejerlejlighed?sortAscending=true",
    "Valby": "https://www.boligsiden.dk/postnummer/2500/solgte/ejerlejlighed?sortAscending=true",
    "Sydvest": "https://www.boligsiden.dk/postnummer/2450/solgte/ejerlejlighed?sortAscending=true",
    "Nordvest": "https://www.boligsiden.dk/postnummer/2150/solgte/ejerlejlighed?sortAscending=true",
}


def get_delta_dataset(config: dict):
    return None


def get_full_dataset(config: dict):
    neighborhood = config["neighborhood"]
    if neighborhood not in base_urls:
        logger.exception("Invalid neighborhood in config!")

    all_scrapers = []
    scraper = BoligScrapper(base_urls[neighborhood], max_area=config["max_area"])
    scraper._add_handle_type("normal")
    scraper.load_all_content()
    scraper.extract_meaningful_data()
    all_scrapers.append(scraper)

    bmarket = BoligMarket(all_scrapers)
    bmarket.clean_data()

    return bmarket.really_interesting_df
