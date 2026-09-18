from datetime import date

from sqlalchemy import select

from app.database.database import AsyncSessionLocal
from app.models.goverment_holiyday_model import GovernmentHoliday


HOLIDAYS = [

    # =========================
    # JANUARY
    # =========================

    {
        "name": "New Year's Day",
        "holiday_date": date(2026, 1, 1),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "New Year's Day",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Pongal",
        "holiday_date": date(2026, 1, 15),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Pongal",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Thiruvalluvar Day",
        "holiday_date": date(2026, 1, 16),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Thiruvalluvar Day",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Uzhavar Thirunal",
        "holiday_date": date(2026, 1, 17),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Uzhavar Thirunal",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Republic Day",
        "holiday_date": date(2026, 1, 26),
        "holiday_type": "NATIONAL",
        "state": None,
        "description": "Republic Day of India",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # MARCH
    # =========================

    {
        "name": "Telugu New Year",
        "holiday_date": date(2026, 3, 19),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Telugu New Year",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Ramzan / Eid-ul-Fitr",
        "holiday_date": date(2026, 3, 21),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Eid-ul-Fitr",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # APRIL
    # =========================

    {
        "name": "Mahavir Jayanti",
        "holiday_date": date(2026, 3, 31),
        "holiday_type": "NATIONAL",
        "state": None,
        "description": "Mahavir Jayanti",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Tamil New Year",
        "holiday_date": date(2026, 4, 14),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Tamil New Year / Dr. B.R. Ambedkar Birthday",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Good Friday",
        "holiday_date": date(2026, 4, 3),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Good Friday",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # MAY
    # =========================

    {
        "name": "May Day",
        "holiday_date": date(2026, 5, 1),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "May Day / Labour Day",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # MAY / JUNE
    # =========================

    {
        "name": "Bakrid",
        "holiday_date": date(2026, 5, 27),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Bakrid / Eid al-Adha",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Muharram",
        "holiday_date": date(2026, 6, 26),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Muharram",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # AUGUST
    # =========================

    {
        "name": "Independence Day",
        "holiday_date": date(2026, 8, 15),
        "holiday_type": "NATIONAL",
        "state": None,
        "description": "Independence Day of India",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Krishna Jayanthi",
        "holiday_date": date(2026, 9, 4),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Krishna Jayanthi",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Vinayaka Chathurthi",
        "holiday_date": date(2026, 9, 14),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Vinayaka Chathurthi",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # SEPTEMBER
    # =========================

    {
        "name": "Milad-un-Nabi",
        "holiday_date": date(2026, 9, 25),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Milad-un-Nabi",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # OCTOBER
    # =========================

    {
        "name": "Gandhi Jayanti",
        "holiday_date": date(2026, 10, 2),
        "holiday_type": "NATIONAL",
        "state": None,
        "description": "Gandhi Jayanti",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Ayudha Pooja",
        "holiday_date": date(2026, 10, 19),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Ayudha Pooja",
        "year": 2026,
        "is_active": True,
    },
    {
        "name": "Vijaya Dasami",
        "holiday_date": date(2026, 10, 20),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Vijaya Dasami",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # NOVEMBER
    # =========================

    {
        "name": "Deepavali",
        "holiday_date": date(2026, 11, 8),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Deepavali",
        "year": 2026,
        "is_active": True,
    },

    # =========================
    # DECEMBER
    # =========================

    {
        "name": "Christmas",
        "holiday_date": date(2026, 12, 25),
        "holiday_type": "STATE",
        "state": "Tamil Nadu",
        "description": "Christmas",
        "year": 2026,
        "is_active": True,
    },
]


async def seed_government_holidays():

    async with AsyncSessionLocal() as session:

        for holiday in HOLIDAYS:

            stmt = select(GovernmentHoliday).where(
                GovernmentHoliday.name == holiday["name"],
                GovernmentHoliday.holiday_date == holiday["holiday_date"],
                GovernmentHoliday.state == holiday["state"],
            )

            result = await session.execute(stmt)

            existing = result.scalar_one_or_none()

            if existing:
                print(
                    f"Already exists: "
                    f"{holiday['name']} - "
                    f"{holiday['holiday_date']}"
                )
                continue

            session.add(
                GovernmentHoliday(**holiday)
            )

        await session.commit()

    print(
        f"Government holiday seed completed. "
        f"Processed {len(HOLIDAYS)} holidays."
    )