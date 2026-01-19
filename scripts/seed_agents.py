from app.database import SessionLocal
from app.models.agent import Agent
from app.database import Base, engine

def seed_agents():
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Check if agents already exist
        existing = db.query(Agent).count()
        if existing > 0:
            print("✅ Agents already exist, skipping seeding.")
            return

        manager = Agent(
            name="John Manager",
            email="john.manager@los.com",
            phone="+1234567890",
            is_available=True
        )
        db.add(manager)
        db.flush()  # generate manager_id

        agents = [
            Agent(
                name="Alice Agent",
                email="alice.agent@los.com",
                phone="+1234567891",
                manager_id=manager.agent_id,
                is_available=True
            ),
            Agent(
                name="Bob Agent",
                email="bob.agent@los.com",
                phone="+1234567892",
                manager_id=manager.agent_id,
                is_available=True
            )
        ]

        db.add_all(agents)
        db.commit()

        print("✅ Agents seeded successfully!")
        print(f"Manager ID: {manager.agent_id}")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding agents: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_agents()
