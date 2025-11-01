from aiogram import Dispatcher,Bot,types,F
from aiogram.filters import Command
from aiogram.types import KeyboardButton,ReplyKeyboardMarkup,InlineKeyboardButton,InlineKeyboardMarkup
from classes import Products
from aiogram.fsm.context import FSMContext
from states import Product

dp = Dispatcher()

bot = Bot(token='8419659250:AAG6KAv1MJqAWS4_W8wxuIBtbrHX_UexD-4')


add = KeyboardButton(text='/add')
get = KeyboardButton(text='/get')

keys = ReplyKeyboardMarkup(keyboard=[[add,get]],resize_keyboard=True)



@dp.message(Command('start'))
async def start(message:types.Message):
    await message.answer('Hello to CRUD bot!',reply_markup=keys)


@dp.message(Command('get'))
async def get_all(message:types.Message):
    prods = Products.get_products()

    for prod in prods:
        await message.answer(f'{prod[1]} \n{prod[2]} \n{prod[3]} \n{prod[4]}')
        await message.answer_photo(photo=prod[5],caption='This is Product')
        buttons = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="Update", callback_data=f"update_{prod[0]}"),
                    InlineKeyboardButton(text="Delete", callback_data=f"delete_{prod[0]}")
                ]
            ])
        
        

@dp.message(Command('add'))
async def add_product(message:types.Message,state:FSMContext):
    await message.answer('Enter Product name')
    await state.set_state(state.prod_name)


@dp.message(Product.prod_name)
async def get_product_name(message: types.Message, state: FSMContext):
    await state.update_data(prod_name=message.text)
    await message.answer('Enter Product description:')
    await state.set_state(Product.quantity)


@dp.message(Product.quantity)
async def get_product_name(message: types.Message, state: FSMContext):
    await state.update_data(quantity=message.text)
    await message.answer('Enter Product description:')
    await state.set_state(Product.description)


@dp.message(Product.description)
async def get_product_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer('Enter product price (in somoni):')
    await state.set_state(Product.price)

@dp.message(Product.price)
async def get_product_price(message:types.Message,state:FSMContext):
    await state.update_data(price = message.text)
    await message.answer('Enter Product Image')
    await state.set_state(Product.image)


@dp.message(F.photo)
async def get_product_image(message:types.Message,state:FSMContext):
    
    data = await state.get_data()
    file_id = message.photo[-1].file_id

    prod = Products.add_product(
        prod_name = data['prod_name'],
        quantity = data['quantity'],
        description = data['description'],
        price = data['price'],
        image = file_id
    )

    await message.answer(f'Product {data['prod_name']} Successfully Added!')
    await state.clear()
 




























@dp.callback_query(lambda c: c.data and c.data.startswith('delete_'))
async def delete_dish_callback(callback: types.CallbackQuery):  
        prod_id = int(callback.data.split('_')[1])
        
        success = await Products.delete_product(prod_id)
        if success:
            await callback.message.delete()
            print('yes')
            await callback.answer("Dish deleted successfully!", show_alert=True)
        else:
            print('no')
            await callback.answer("Failed to delete dish", show_alert=True)



if __name__ == '__main__':
    dp.run_polling(bot)