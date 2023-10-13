from sqlalchemy import create_engine, ForeignKey, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///freebies.db')
Session = sessionmaker(bind=engine)
session = Session()

company_dev = Table(
    'company_devs',
    Base.metadata,
    Column('id', Integer(), primary_key=True),
    Column('company_id', ForeignKey('companies.id')),
    Column('dev_id', ForeignKey('devs.id')),
    extend_existing=True,
)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    devs = relationship('Dev', secondary=company_dev, back_populates='companies')
    freebies = relationship('Freebie', backref=backref('company'))

    def __repr__(self):
        return f'<Company {self.name}>'
    
    def give_freebie(self, dev, item_name, value):
        if isinstance(dev, Dev):
            new_freebie = Freebie(
                item_name=item_name,
                value=value,
                dev_id=dev.id,
                company_id=self.id
            )    
            session.add(new_freebie)
            session.commit()
        else:
            return TypeError("dev must be an instance of the Dev class.")
    
    @classmethod
    def oldest_company(cls):
        return session.query(Company).order_by(Company.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name= Column(String())

    companies = relationship('Company', secondary=company_dev, back_populates='devs')
    freebies = relationship('Freebie', backref=backref('dev'))

    def __repr__(self):
        return f'<Dev {self.name}>'
    
    def received_one(self, item_name):
        return item_name in [freebie.item_name for freebie in self.freebies]
    
    def give_away(self, dev, freebie):
        if isinstance(freebie, Freebie):
            if freebie in self.freebies:
                if isinstance(dev, Dev):
                    freebie.dev = dev
                    session.add(freebie)
                    session.commit()
                else:
                    return TypeError("dev must be an instance of the Dev class")
            else:
                return ValueError(f"The {freebie.item_name} freebie does not belong to {self.name}.")
        else: 
            return TypeError("freebie must be an instance of the Freebie class.")
    
class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    dev_id = Column(Integer(), ForeignKey('devs.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'))

    def __repr__(self):
        return f'<Freebie {self.item_name}>'
    
    def print_details(self):
        return f"{self.dev.name} owns a {self.item_name} from {self.company.name}"
