from loguru import logger


class OutOfStock(Exception):
    logger.error(
        "Can't allocate this orderline in this batch. Order quantity is higher than the stock quantity."
    )


class InvalidSku(Exception):
    logger.error("Invalid SKU. This product is not available.")
