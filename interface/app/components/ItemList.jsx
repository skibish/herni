import React from 'react';
import Item from './Item.jsx';

class ItemList extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    var itemNodes = this.props.products.map((product) => {
      let isSelectable = (product.count > 0);
      return (
        <Item
          key={product.slot}
          slot={product.slot}
          name={product.name}
          price={product.price}
          count={product.count}
          isSelectable={isSelectable}
          onSelectClick={this.props.onItemSelection}
          selectedItem={this.props.selectedItem}
           />
        );
    });

    return (
      <div className="items">
        {itemNodes}
      </div>
    );
  }
}

export default ItemList;
