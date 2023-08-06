# MODULES
from contextlib import AbstractContextManager
from logging import Logger
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

# PYDANTIC
from pydantic import BaseModel

# SQLALCHEMY
from sqlalchemy.orm import Session, InstrumentedAttribute

# UTILS
from session_repository.utils import (
    _FilterType,
    apply_no_load,
    apply_filters,
    apply_order_by,
    apply_limit,
    apply_pagination,
)


T = TypeVar("T", bound=BaseModel)


class SessionRepository:
    def __init__(
        self,
        session_factory: Callable[..., AbstractContextManager[Session]],
        logger: Logger,
        literal_binds: bool = True,
    ) -> None:
        self._session_factory = session_factory
        self._logger = logger
        self._literal_binds = literal_binds

    def _select(
        self,
        model,
        model_returned: Optional[Type[T]] = None,
        filters: Optional[_FilterType] = None,
        disabled_relationships: Optional[Dict[InstrumentedAttribute, Any]] = None,
        current_session: Optional[Session] = None,
    ) -> Union[Tuple[List[Any], str], List[Any], Any]:
        def _select_from_session(session: Session):
            query = session.query(model)
            query = apply_no_load(query=query, relationship_dict=disabled_relationships)
            query = apply_filters(query=query, filter_dict=filters)
            results = query.first()

            if self._logger is not None:
                query_compiled = query.statement.compile(
                    compile_kwargs={"literal_binds": self._literal_binds}
                )
                self._logger.info(query_compiled.string)

            if results is None:
                return

            mapped_results = (
                model_returned.from_orm(results)
                if model_returned is not None
                else results
            )

            return mapped_results

        if current_session is not None:
            results = _select_from_session(session=current_session)
        else:
            with self._session_factory() as session:
                results = _select_from_session(session=session)

        return results

    def _select_all(
        self,
        model,
        model_returned: Optional[Type[T]] = None,
        filters: Optional[_FilterType] = None,
        disabled_relationships: Optional[Dict[InstrumentedAttribute, Any]] = None,
        page: Optional[int] = None,
        per_page: Optional[int] = None,
        order_by: Optional[Union[List[str], str]] = None,
        direction: Optional[str] = None,
        limit: int = None,
        current_session: Optional[Session] = None,
    ) -> Union[Tuple[List[Any], str], List[Any]]:
        def _select_from_session(session: Session):
            query = session.query(model)
            query = apply_no_load(query=query, relationship_dict=disabled_relationships)
            query = apply_filters(query=query, filter_dict=filters)
            query = apply_order_by(
                query=query, model=model, order_by=order_by, direction=direction
            )
            query = apply_limit(query=query, limit=limit)
            query, pagination = apply_pagination(
                query=query, page=page, per_page=per_page
            )

            results = query.all()

            if self._logger is not None:
                query_compiled = query.statement.compile(
                    compile_kwargs={"literal_binds": self._literal_binds}
                )
                self._logger.info(query_compiled.string)

            if results is None:
                return

            mapped_results = (
                [model_returned.from_orm(res) for res in results]
                if model_returned is not None
                else results
            )

            if pagination is None:
                return mapped_results

            return mapped_results, pagination

        if current_session is not None:
            results = _select_from_session(session=current_session)
        else:
            with self._session_factory() as session:
                results = _select_from_session(session=session)

        return results

    def _update(
        self,
        model,
        values: Dict,
        filters: Optional[_FilterType] = None,
        flush: bool = False,
        commit: bool = False,
        current_session: Optional[Session] = None,
    ):
        def _update_from_session(session: Session):
            rows = self._select(
                model=model,
                filters=filters,
                current_session=session,
            )

            if len(rows) == 0:
                return rows

            for row in rows:
                for key, value in values.items():
                    setattr(row, key, value)

            if flush:
                session.flush()
            if commit:
                session.commit()

            [session.refresh(row) for row in rows]

            return rows

        if current_session is not None:
            results = _update_from_session(session=current_session)
        else:
            with self._session_factory() as session:
                results = _update_from_session(session=session)

        return results

    def _add(
        self,
        session: Session,
        data,
        flush: bool = False,
        commit: bool = False,
        current_session: Optional[Session] = None,
    ):
        def _add_from_session(session: Session):
            session.add_all(data) if isinstance(data, list) else session.add(data)
            if flush:
                session.flush()
            if commit:
                session.commit()

            session.refresh(data)

            return data

        if current_session is not None:
            results = _add_from_session(session=current_session)
        else:
            with self._session_factory() as session:
                results = _add_from_session(session=session)

        return results

    def _delete(
        self,
        model,
        filters: Optional[_FilterType] = None,
        flush: bool = True,
        commit: bool = False,
        current_session: Optional[Session] = None,
    ) -> bool:
        def _delete_from_session(session: Session):
            rows: List[BaseModel] = self._select(
                model=model, filters=filters, current_session=session
            )

            if len(rows) == 0:
                return False

            for row in rows:
                session.delete(row)

            if flush:
                session.flush()
            if commit:
                session.commit()

            return True

        if current_session is not None:
            results = _delete_from_session(session=current_session)
        else:
            with self._session_factory() as session:
                results = _delete_from_session(session=session)

        return results
