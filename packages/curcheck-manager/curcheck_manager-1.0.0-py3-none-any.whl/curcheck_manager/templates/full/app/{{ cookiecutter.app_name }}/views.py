from curcheck import SiteRouter

router = SiteRouter(
    domain="https://pypi.org",
    is_spa=False
)


@router.page(url="/project/curcheck/")
async def start(tree):
    print(
        tree.xpath("//span[@id='pip-command']/text()")
    )
