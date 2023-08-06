from elefantolib_fastapi import middleware

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession


class PageNumberPagination:
    def __init__(self, session: AsyncSession, query: Select, page: int, page_size: int):
        self.session = session
        self.query = query
        self.page = page
        self.page_size = page_size
        self.request = middleware.request_object.get()
        # computed later
        self.number_of_pages = 0
        self.next_page = ''
        self.previous_page = ''

    def _get_next_page(self) -> str | None:
        if self.page >= self.number_of_pages:
            return

        return str(self.request.url.include_query_params(page=self.page + 1))

    def _get_previous_page(self) -> str | None:
        if self.page == 1 or self.page > self.number_of_pages + 1:
            return

        return str(self.request.url.include_query_params(page=self.page - 1))

    async def get_response(self) -> dict:
        limit = self.page_size
        offset = (self.page - 1) * self.page_size

        query = self.query.limit(limit).offset(offset)

        return {
            'count': await self._get_total_count(),
            'next': self._get_next_page(),
            'previous': self._get_previous_page(),
            'results': [i for i in await self.session.scalars(query)],
        }

    def _get_number_of_pages(self, count: int) -> int:
        rest = count % self.page_size
        quotient = count // self.page_size

        return quotient if not rest else quotient + 1

    async def _get_total_count(self) -> int:
        count = await self.session.scalar(select(func.count()).select_from(self.query.subquery()))
        self.number_of_pages = self._get_number_of_pages(count)

        return count


async def paginate(db_session, query: Select, page: int, page_size: int) -> dict:
    async with db_session as session:
        paginator = PageNumberPagination(session, query, page, page_size)
        return await paginator.get_response()
