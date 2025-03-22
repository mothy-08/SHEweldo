import asyncio
import aiohttp
import random
from enum import StrEnum, auto
from datetime import datetime, timedelta

# Define the enums
class Department(StrEnum):
    EXECUTIVE_LEADERSHIP = auto()
    OPERATIONS = auto()
    FINANCE_ACCOUNTING = auto()
    HUMAN_RESOURCES = auto()
    LEGAL_COMPLIANCE = auto()
    MARKETING_SALES = auto()
    CUSTOMER_SERVICE_SUPPORT = auto()
    TECHNOLOGY_IT = auto()
    PRODUCT_RD = auto()
    SUPPLY_CHAIN_LOGISTICS = auto()
    OTHER = auto()

class Gender(StrEnum):
    MALE = auto()
    FEMALE = auto()
    NONBINARY = auto()
    OTHER = auto()

# List of company hashes
# List of company hashes
company_hashes = [
    "0ffbf43dcc7e1447cd7ba7cf043778743bba0005e49300c7469ce7dd2e064383",
    "90fee001af1e7552b9bebbb504f813e5643251e7e48dce54cbefc194b46b75a7",
    "117d81d9398791bd261506ed6d21b78db59e79056177957f5314cb016b994609",
    "7fbd2efc888807a264ee3b433cfbce9e82d775c3a5c26413325f95236825751e",
    "71c5cda377b55e2cee3b73a8cfe5cdd95f6b6c41c9cc21d64b71a5be1a7a2686",
    "f21139912a20bc5206e7148d0deeea0ddebb0a8fb016cb513645b450d7500d92",
    "af76734534d08764ef711ca95b1f32bfc1309ee45562518b23c989938de9dd12",
    "1c54c59ea32a966edd98078f5a5d023b0bcea0beaa376e0705ad7a04fbf5616b",
    "df603caeec5cc949fbaa7fdf92aa4dbec9e1637063fb554ea5ad2ebdc2934208",
    "81cc214dccca82208d8becfe4aa1ae0f22a463e7d8b00fd1b868a27785803da3",
    "279aad8dad8b46c3c550191c0b65ed5265a059c19e5fc0efbf15ad0f75ccee3f",
    "5725ebb81ff553367c7719bd327d51a88ad40336c669dff7f54dc0b3dcbafb79",
    "22580d8d0310d4e74951ab028bafb2838535d7d77cfb081c3b9a23de0132aa43",
    "8f2d3ac6db1238d14178764186c3d67bf9a83c76e44e84dd56da5fad2500cb48",
    "d1e85daa8b14f6b0dc03d374d3de796539444c8a65fd01d5fe338893a4067f29",
    "b1db9fed8204f392974a4025832e3266f4cb88f612a504faafb8f5f7f98f138a",
    "2ed25de3d7b00587a464681b329233460909005cb4e5c8b2b358dde0c2956b35",
    "5fd117a218a0e5897818d98c319696ab832305450a8e381805255b163d2223c7",
    "7502df80265f177c1bf97c76c95fd12dfdab9ea50b3917804146eec424f61e97",
    "bf5a00a550d3c4c41f44c52f69dd346df4c23c289156922340f19ef021d241e2",
    "fbf5190f407531b39d97fd491627f37d47f53895dea3be74713136d31eb23edf",
    "862f5f8dc1db80e5611095f4355acc9eacfd226bef99f3bd6d3d5d4e9e571d95",
    "6030fb9b22d56c50e39c58810252cd8f9ac13a28941d6fb24fad5b57adf90c73",
    "e4db092e98e5451a6c9b3c627c105fdccc601b013fd6c9934b185cb04a919591",
    "7f3b2f85842d9455551ea227189fa689e64fc0b080f6df7758a29d8d2073f0fb",
    "4d8971a86c0fa80ab0a51897dfb09f2e3df47db216739cf15f112c41ca0598c6",
    "ff296938f85b087cae2912cdefa49f26c1f973604eac4f5e544bb8166d150a85",
    "aab19d4830449aeb9b6de4315887cf320b9b4641a8d9ff803d549cccb8dcf0c5",
    "43a08dae13f82d487ab1d9454087240c584d40ac499148bd08b3c8a035563707",
    "8de25be579dc479e8d9be55ae1c11a2eb8a326f392c38e855210841f2b136669",
    "7b4bc342e489b5ff8b250ed1bb9ddb8924f27213a36308017e8863ed64c4fa64",
    "c7dc83a3228c80d906123ba34ff886de33bc87e4b2b295aa468ff9e1a8321098",
    "4e603252076cc956f056f66fc7a113cb23617290b3b45d39b8bfc8c84502a18c",
    "e8f20df09600a4b55f70f2072274085c1879605fabbf868327dc7a3be1faba74",
    "7350fbd30e524cff5f6145dca74cd8146e5575e7f96400dee5af0b71531e33a0",
    "5ac920827a7d460bf0439702cdd69beda014a2584e879c48b107fce041a108a3",
    "4862efe78eb6295520c44295465417c5471c841e222e4eea51562d3e642a64b4",
    "0f3d20eb73f5cc77a3d79fda7731de083588122f4cb5785181238990c35cbe76",
    "c9d840381926a19f4602c53996358eb54596ba59aa9767a89119be07e37b1cd9",
    "1dde8036caba7e72bb974416887f7fdc568a3523ad9d8ba0ff14d5137860fe21",
    "2cf431118a1848da6dd64a04678dde92ad9d744cc0855997c230b1f2d0e19ef8",
    "be417630516521d8139350e3da713291aac2ecc891347eb9c408f5a0ff03782c",
    "f6047660ccdd06e4d4b5d6d6882e6b66626df8b00731de0e7efa9abfa86351d8",
    "96047910535d7ce3ab7c952005a5e89feb841a46384d1a57729f67f54224e48d",
    "38a7ab9b04ff65ce2ea05a9d2db08631ea1225657e06d256e6cd7ff79f79ba47",
    "d385b6fedca739dbfa7e115b1c01f48a58898768bb525eae457dd0868c4982cd",
    "f6b487511cdd50a5776a3e44eba8a4b9e9960b0c63e078f8fe2806a216eb3dee",
    "7ad6e0eb2c8a9bde020ce15dabba044e2d479f1433dbef8dce61aa5f9b4c50a1",
    "9e0a34047453c533a4013e6e42dab965176e6550cf7fec48bccb6155c17d846d",
    "cbc5298eb7002eb36c9900f588854a61b39fcb193ebbe47602dac26c8fb64816",
    "5038cad3ae4f2573b6ca5b592e0d30b4ac316859fa64dd8238fbbb41ab4c9745",
    "9a55421bcf2f5646f7d458fa8d28badb51b59f233b6311105c8758363dfac9bf",
    "33db4243e0a82ff2e4550ddf1cc63fc3d7b1e70e322e3dde6eb1c59cfa817f6b",
    "1e39325167d771ca4758efdc50f9c8c90b2eb54499d25da368edb20c5c8cf19b",
    "17d49e7de09ff227c79afe5ac77f7df8667cf5b05755a08ea7155c74c990ef51",
    "7b6c8605bc5567da17ca3051e56dcbfdd997a8af26d626f6ec4028d37602f69c",
    "09b6b22d0c5c4cd0d767ec43bc91c23bf0996ce535b580e16ba353dda6f04d0c",
    "aeb5e8517a15d84d367ebe27662d108dd8039b71d46399df9e0eda0867f8eaa8",
    "f3dee0f5b409ae65e895f0855309802f2f914fb45615f6be2dff3710dcf46dad",
    "ebca59dd106a36f7ee9b6fcdbf74270c1f07c1e5414ba07c4532b80eab71cdf8",
    "7447f0bea7c50c222066bfdd055d2f36ee65a85c2d8aeca6f0d1867a54c24de6",
    "b955ddf9b7aba185eef499911f84bfc07dfbac72840c4fbd83f159c666b82cac",
    "9bb79c4f15a04a4b600721252075a6374628dffb816a9e59d185d000fd23bf51",
    "49e24304fd46e73dfddef4aad7dcae91f10a758d713d804582fbd92b7b1660b8",
    "f009f6fe64a01612e0159bbc5c5b20c8d9678075c9b1af8216c5102388f865d0",
    "0f6f3bcadc553cbeed473a2da7fda511e13eca608f3460a015004eb06c445e67",
    "d91c1a68d1e3030d84029c2f5da09df04661e2d68eb02b0d6a4803d05b5b53eb",
    "4a16be8be8517d02c641b59d0934665869e78acd5a81e28cd210489fed5909e8",
    "b9f27f331cca41ee5f49b97d4753a0aac23280d9c6856521fa7bb6681e265495",
    "c32da22c0939b60de96066105195dc599e06a4cd5adf20c0d0d09194e8631bdf",
    "fd3c76ed938708a3bacd0bb18231e43427d20aabba4b59053f77cbcbecebe68e",
    "055bc609629c5c200cd903588b78325a8d11f00c1fd2350126016b38d8b55c4c",
    "26cd02c4b4dac4854243c2d32e577f275530e53f77cfcc781789355fb3c081a3",
    "08bd12db38a4cdb4eaf94d063e34e41bf50cc5de77e28efba5647546bc847e68",
    "e2a223c76acfb099576580a1e9cc11522d0e3a0372ec1f9ccdf4b1033c33a47b",
    "e9c43e5871b6624b49b115317318a3320be730d82e220c1861bf2017deae83d6",
    "bce4859bbc9b4cc7c32e8df17f8d786e249af056604e441399955bf42823f32c",
    "9dc11f16e52b9eb91450bdc4ba237aede376e47f56ae5513f149f52842ff1407",
    "fcdf3d80abac1c2197e29fe304a99c5318c412f6f617f8db05675b0c762e504f",
    "71ec8bd132598b5937d02a0baa684d5ecfd8753d8da5d96aa6f864127da6e6fc",
    "5b92b253eaf411e89897c840017d99e1dc4bfd33a41a1196e71c0a375f7985f6",
    "fc7ca4fab25fbd0c29c78d6abce32c3dc17dc803a538970ead3d2aef9baaf26f",
    "479ab0e015bb245f2defe616f20a77bfedca097d2fb8960f1682ad8340828ed9",
    "a67d3a6cf42f6787de2c1c220ec71911393acfbcfb2baa95d01c62175c8abcce",
    "da96fc9534d23a147bc229d1e4549ee86416a883e1bd34feff4332931472a071",
    "9bf3037ee05ee02e54deb0d569c728024609c7b81f7fea82ae9be5d9c103bc6c",
    "25a58c5ccbbb03f4e32e7d9f7b31d3aa4306ab424903dddce34f4998505319e8",
    "b6a76f1a25cb1185f6bef36101d31f23383ccbf23191ab7c5f31e1378f64cb64",
    "6d5e4a8a3a20956cfd84770716b72539e1c0d51f1b47a696e1698d7569a712dc",
    "70e5254eb3e3cfea8e6ddedc603d6eae80e18a7d8d8d306c4b26033bf3a8cd34",
    "d9461130489eb95a5ec28635f98273174b4653ae4b4dfb55d7ef0db50acbecff",
    "3d0d2bd10d83a526ea7a3914c873e8aec77c5bfba5bfca990f20c38ef3a65837",
    "1198120b4ae601bdc3fd9bacdd98527eaa4aefcbc5e37c17c55c946fdef6ca2c",
    "433d59050df24907662d5ba06b8a3a9799c6edc5b5ffe8e33e508bfe819e3628",
    "79ca9451f175dbf5f75d7778217c68829ab5a454a0055b5799f775099751b154",
    "59a3b31ccdc1732e5c8270954f081a3202783e9a7e42d4620f3af6e60324bfb1",
    "b93c08aa50bc2df0f272c9e1eac8aeea5332406d610239cd1f6ec4a247d00b88",
    "7a3b389bd719214d3cfd416b7808390707dd6f543d717afdff4bb997d53dfada"
]

job_titles = [
    "Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer",
    "UX Designer", "Business Analyst", "Sales Manager", "Marketing Specialist",
    "HR Manager", "Financial Analyst", "Legal Counsel", "Customer Support Representative"
]

url = "http://localhost:5000/api/salaries/submit"

def generate_salary_data():
    company_hash = random.choice(company_hashes)
    years_at_the_company = random.randint(1, 10)
    total_experience = years_at_the_company + random.randint(1, 10)
    salary_amount = random.randint(15000, 40000)
    gender = random.choice(list(Gender)).value
    submission_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
    is_well_compensated = random.choice([True, False, False, False])
    department = random.choice(list(Department)).value
    job_title = random.choice(job_titles)
    
    return {
        "company_hash": company_hash,
        "years_at_the_company": years_at_the_company,
        "total_experience": total_experience,
        "salary_amount": salary_amount,
        "gender": gender,
        "submission_date": submission_date,
        "is_well_compensated": is_well_compensated,
        "department": department,
        "job_title": job_title
    }

def generate_salary_dataset(num_records):
    return [generate_salary_data() for _ in range(num_records)]

async def submit_salary_data(session, data, semaphore):
    async with semaphore:
        try:
            async with session.post(url, json=data) as response:
                if response.status == 201:
                    print(f"Submitted salary data for company hash: {data['company_hash']}")
                else:
                    print(f"Failed to submit salary data: {response.status}, {await response.text()}")
        except Exception as e:
            print(f"Error submitting data: {e}")

async def main(num_submissions):
    dataset = generate_salary_dataset(num_submissions)
    
    semaphore = asyncio.Semaphore(100)
    
    connector = aiohttp.TCPConnector(limit=100)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for data in dataset:
            task = asyncio.create_task(submit_salary_data(session, data, semaphore))
            tasks.append(task)
        await asyncio.gather(*tasks)

# Run the script
if __name__ == "__main__":
    import time

    num_submissions = 2500

    start_time = time.time()
    asyncio.run(main(num_submissions))
    end_time = time.time()

    print(f"Total time: {end_time - start_time:.2f} seconds")